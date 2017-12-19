from bisect import insort_left
import os
import logging
import numpy as np
logger = logging.getLogger(os.path.basename(__file__))


class Minibatch(object):
    '''
    The selected labels (i.e. classes for prediction).
    Per default, all available labels are selected.

    The order of the labels list defines the order of the
    labels layer in the probability map (i.e. the classification result
    matrix) that can be exported with put_probmap_data().
    '''
    labels = []

    '''
    Returns the selected image channels.
    Per default, all available channels are selected.

    The order of the channels list defines the order of the
    channels layer in the pixels (accessed with get_pixels()).
    Pixels have the dimensionality (channels, z, x, y)

    >>> from yapic_io.factories import make_tiff_interface
    >>>
    >>> pixel_image_dir = 'yapic_io/test_data/tiffconnector_1/im/'
    >>> label_image_dir = 'yapic_io/test_data/tiffconnector_1/labels/'
    >>> savepath = 'yapic_io/test_data/tmp/'
    >>>
    >>> tile_size = (1, 5, 4)
    >>> # make training_batch mb and prediction interface p: upon object initialization all available image channels are set
    >>> mb, p = make_tiff_interface(pixel_image_dir, label_image_dir, savepath, tile_size) #upon object initialization all available image channels are set
    >>>
    >>>
    >>> p.channel_list # we have 3 channels in the prediction interface
    [0, 1, 2]
    >>>
    >>> p[0].pixels().shape # accordingly, we have 3 channels in the 5D pixels tile (n, c, z, x, y)
    (10, 3, 1, 5, 4)
    >>>
    '''
    channel_list = []

    def __init__(self, dataset, batch_size, size_zxy, padding_zxy=(0, 0, 0)):
        '''
        :param dataset: dataset object, to connect to pixels and labels weights
        :type dataset: Dataset
        :param batch_size: nr of tiles
        :type batch_size: int
        :param size_zxy: 3d tile size (size of classifier output tmeplate)
        :type size_zxy: tuple (with length 3)
        :param padding_zxy: growing of pixel tile in (z, x, y).
        :type padding_zxy: tuple (with length 3)
        :param augment: if True, tiles are randomly rotatted and sheared
        :type augment: bool
        :param rotation_range: range of random rotation in degrees (min_angle, max_angle)
        :type rotation_angle: tuple (with length 2)
        :param shear_range: range of random shear in degrees (min_angle, max_angle)
        :type shear_angle: tuple (with length 2)
        :param equalized: if True, less frequent labels are favored in randomized tile selection
        :type equalized: bool
        '''
        self._dataset = dataset
        self._batch_size = batch_size
        self.normalize_mode = None
        self.global_norm_minmax = None

        self.float_data_type = np.float32  # type of pixel and weight data

        np.testing.assert_equal(len(size_zxy), 3, 'len of size_zxy be 3: (z, x, y)')
        self.tile_size_zxy = size_zxy

        np.testing.assert_equal(len(padding_zxy), 3, 'len of padding_shoule be 3: (z, x, y)')
        self.padding_zxy = padding_zxy

        # imports all available channels by default
        self.channel_list = self._dataset.channel_list()
        # imports all available labels by default
        self.labels = self._dataset.label_values()

    def set_normalize_mode(self, mode_str, minmax=None):
        '''
        local : scale between 0 and 1 (per minibatch, each channel
                separately)
        local_z_score : mean to zero, scale by standard deviation
                        (per minibatch, each channel separately)
        global : scale minmax=(min, max) between 0 and 1
                 whole dataset, each channel separately
        minmax : tuple of minimum and maximum pixel value for global
                 normalization. e.g (0, 255) for 8 bit images
        '''

        if mode_str in ('local_z_score', 'local', 'off'):
            self.normalize_mode = mode_str

        elif mode_str == 'global':
            if minmax is None:
                err_msg = 'Missing minmax for defining global minimum' + \
                          'and maximum for normalization: (min, max)'
                raise ValueError(err_msg)
            self.global_norm_minmax = minmax
            self.normalize_mode = mode_str

        else:
            err_msg = '''Wrong normalization mode argument: {}. '''.format(mode_str) + \
                      '''choose between 'local', 'local_z_score', 'global' and 'off' '''
            raise ValueError(err_msg)

    def remove_channel(self, channel):
        '''
        Removes a pixel channel from the selection.
        :param channel: channel
        :returns: bool, True if channel was removed from selection

        >>> from yapic_io import TiffConnector, Dataset, PredictionBatch
        >>> import tempfile
        >>>
        >>> pixel_image_dir = 'yapic_io/test_data/tiffconnector_1/im/'
        >>> label_image_dir = 'yapic_io/test_data/tiffconnector_1/labels/'
        >>> savepath = tempfile.TemporaryDirectory()
        >>>
        >>> tile_size = (1, 5, 4)
        >>> #upon object initialization all available image channels are set
        >>> c = TiffConnector(pixel_image_dir, label_image_dir, savepath=savepath.name)
        >>> p = PredictionBatch(Dataset(c), 10, tile_size, padding_zxy=(0,0,0))
        >>>
        >>> p.channel_list #we have 3 channels
        [0, 1, 2]
        >>> p[0].pixels().shape #accordingly, we have 3 channels in the 5D pixels tile (n, c, z, x, y)
        (10, 3, 1, 5, 4)
        >>>
        >>> p.remove_channel(1) #remove channel 1
        >>> p.channel_list #only 2 channels selected
        [0, 2]
        >>> p[0].pixels().shape #only 2 channels left in the pixel tile
        (10, 2, 1, 5, 4)

        '''
        if channel not in self.channel_list:
            raise ValueError('not possible to remove channel %s from channel selection %s'
                             % (str(channel), str(self.channel_list)))
        self.channel_list.remove(channel)

    def add_channel(self, channel):
        '''
        Adds a pixel-channel to the selection.
        '''
        if channel in self.channel_list:
            logger.info('channel already selected %s', channel)
            return False

        if channel not in self._dataset.channel_list():
            msg = 'Not possible to add channel {} from dataset channels {}'
            raise ValueError(msg.format(channel, self._dataset.channel_list()))

        insort_left(self.channel_list, channel)
        return True

    def remove_label(self, label):
        '''
        Removes a label class from the selection.

        :param label: label
        :returns: bool, True if label was removed from selection

        >>> from yapic_io import TiffConnector, Dataset, PredictionBatch
        >>> import tempfile
        >>>
        >>> pixel_image_dir = 'yapic_io/test_data/tiffconnector_1/im/'
        >>> label_image_dir = 'yapic_io/test_data/tiffconnector_1/labels/'
        >>> savepath = tempfile.TemporaryDirectory()
        >>>
        >>> tile_size = (1, 5, 4)
        >>> #upon object initialization all available image channels are set
        >>> c = TiffConnector(pixel_image_dir, label_image_dir, savepath=savepath.name)
        >>> p = PredictionBatch(Dataset(c), 10, tile_size, padding_zxy=(0,0,0))
        >>>
        >>> p.labels #we have 3 label classes
        [1, 2, 3]
        >>> p.remove_label(2) #remove label class 109
        >>> p.labels #only 2 classes remain selected
        [1, 3]

        '''
        if label not in self.labels:
            msg = 'Not possible to remove label {} from label selection {}'
            raise ValueError(msg.format(label, self.labels))

        self.labels.remove(label)

    def add_label(self, label):
        '''
        Adds a label class to the selection.

        >>> from yapic_io import TiffConnector, Dataset, PredictionBatch
        >>> import tempfile
        >>>
        >>> pixel_image_dir = 'yapic_io/test_data/tiffconnector_1/im/'
        >>> label_image_dir = 'yapic_io/test_data/tiffconnector_1/labels/'
        >>> savepath = tempfile.TemporaryDirectory()
        >>>
        >>> tile_size = (1, 5, 4)
        >>> #upon object initialization all available image channels are set
        >>> c = TiffConnector(pixel_image_dir, label_image_dir, savepath=savepath.name)
        >>> p = PredictionBatch(Dataset(c), 10, tile_size, padding_zxy=(0,0,0))
        >>>
        >>> p.labels #we have 3 label classes
        [1, 2, 3]
        >>> p.remove_label(2) #remove label class 2
        >>> p.labels #only 2 classes remain selected
        [1, 3]
        >>> p.remove_label(1) #remove label class 1
        >>> p.labels #only 1 class remains selected
        [3]
        >>> p.add_label(1)
        True
        >>> p.labels
        [1, 3]
        >>> p.add_label(2)
        True
        >>> p.labels
        [1, 2, 3]


        '''
        if label in self.labels:
            logger.info('Label class already selected {}', label)
            return False

        if label not in self._dataset.label_values():
            msg = 'Not possible to add label class {} from dataset label classes {}'
            raise ValueError(msg.format(label, self._dataset.label_values()))

        insort_left(self.labels, label)
        return True

    def _normalize(self, pixels):
        '''
        to be called by the self.pixels() function
        '''

        if self.normalize_mode is None:
            return pixels

        if self.normalize_mode == 'off':
            return pixels

        if self.normalize_mode == 'global':
            center_ref = np.array(self.global_norm_minmax[0])
            scale_ref = np.array(self.global_norm_minmax[1])

        if self.normalize_mode == 'local':
            # scale between 0 and 1
            #(data-minval)/(maxval-minval)
            # percentiles are used for minval and maxval to be robust
            # against outliers
            max_ref = np.percentile(pixels, 99, axis=(0, 2, 3, 4))
            min_ref = np.percentile(pixels, 1, axis=(0, 2, 3, 4))

            center_ref = min_ref
            scale_ref = max_ref - min_ref

        if self.normalize_mode == 'local_z_score':
             #(data-mean)/std
            center_ref = pixels.mean(axis=(0, 2, 3, 4))
            scale_ref = pixels.std(axis=(0, 2, 3, 4))

        pixels_centered = (pixels.swapaxes(1, 4) -
                           center_ref).swapaxes(1, 4)

        if (scale_ref == 0).all():
            # if scale_ref is zero, do not scale to avoid zero
            # division
            return pixels_centered
        # scale by scale reference
        return (pixels_centered.swapaxes(1, 4) /
                scale_ref).swapaxes(1, 4)
