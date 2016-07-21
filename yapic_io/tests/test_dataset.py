from unittest import TestCase
import os
import numpy as np

from yapic_io.tiffconnector import Tiffconnector
from yapic_io.dataset import Dataset
from yapic_io.utils import get_template_meshgrid
import yapic_io.dataset as ds

import logging
logger = logging.getLogger(os.path.basename(__file__))

base_path = os.path.dirname(__file__)

class TestDataset(TestCase):
    def test_n_images(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        c = Tiffconnector(img_path,'path/to/nowhere/')
        d = Dataset(c)

        self.assertEqual(d.n_images, 3)
        # img_filenames = [\
        #         ('6width4height3slices_rgb.tif',)\
        #         , ('40width26height3slices_rgb.tif',)\
        #         , ('40width26height6slices_rgb.tif',)\
        #         ]

        
        

        


    def test_get_padding_size_1(self):

        shape = (7, 11)
        pos = (5, 5)
        size = (3, 5)
        res = ds.get_padding_size(shape, pos, size)
        self.assertEqual([(0, 1), (0, 0)], res)


    def test_get_padding_size_2(self):

        shape = (7, 11)
        pos = (-3, 0)
        size = (3, 5)

        res = ds.get_padding_size(shape, pos, size)
        self.assertEqual([(3,0),(0,0)], res) 

    def test_get_padding_size_3(self):

        shape = (7, 11, 7)
        pos = (5, 5, 5)
        size = (3, 5, 3)
        res = ds.get_padding_size(shape, pos, size)
        self.assertEqual([(0, 1), (0, 0), (0, 1)], res)

    def test_get_padding_size_3(self):

        shape = (7, 11, 7, 1)
        pos = (5, 5, 5, 0)
        size = (3, 5, 3, 1)
        res = ds.get_padding_size(shape, pos, size)
        self.assertEqual([(0, 1), (0, 0), (0, 1), (0, 0)], res)    

        

    def test_get_dist_to_upper_img_edge(self):


        pos = (3, 1)
        shape = (5, 4)
        val = np.array([1, 2])
        res = ds.get_dist_to_upper_img_edge(shape, pos)
        self.assertTrue((val == res).all())


        pos = (4, 3)
        shape = (5, 4)
        val = np.array([0, 0])
        res = ds.get_dist_to_upper_img_edge(shape, pos)
        self.assertTrue((val == res).all())



    def test_calc_inner_template_size_1(self):

        shape = (7, 11)
        pos = (-4, 8)
        size = (16, 9)

        pos_val = (0, 5)
        size_val = (7, 6)
        pos_tpl_val = (0, 3)
        pos_out, size_out, pos_tpl, padding = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)    
        self.assertEqual(pos_tpl_val, pos_tpl)  
        self.assertEqual(padding, [(4,5),(0,6)])

    def test_calc_inner_template_size_2(self):

        shape = (7, 11)
        pos = (-4, -1)
        size = (5, 8)

        pos_val = (0, 0)
        size_val = (4, 7)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(4,0),(1,0)])        

    def test_calc_inner_template_size_3(self):

        shape = (7, 11)
        pos = (-2, -3)
        size = (3, 4)

        pos_val = (0, 0)
        size_val = (2, 3)
        
        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(2,0),(3,0)])        

    def test_calc_inner_template_size_4(self):

        shape = (7, 11)
        pos = (-5, 2)
        size = (6, 4)

        pos_val = (0, 2)
        size_val = (5, 4)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(5,0),(0,0)])        


    def test_calc_inner_template_size_5(self):

        shape = (7, 11)
        pos = (2, -4)
        size = (3, 8)

        pos_val = (2, 0)
        size_val = (3, 4)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(0,0),(4,0)])        
    def test_calc_inner_template_size_6(self):

        shape = (7, 11)
        pos = (2, 9)
        size = (3, 6)

        pos_val = (2, 7)
        size_val = (3, 4)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,2))
        self.assertEqual(pd, [(0,0),(0,4)]) 

    def test_calc_inner_template_size_7(self):

        shape = (7, 11)
        pos = (2, 9)
        size = (6, 5)

        pos_val = (2, 8)
        size_val = (5, 3)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,1))
        self.assertEqual(pd, [(0,1),(0,3)]) 

    def test_calc_inner_template_size_8(self):

        shape = (7, 11)
        pos = (5, 9)
        size = (5, 6)

        pos_val = (4, 7)
        size_val = (3, 4)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (1,2))
        self.assertEqual(pd, [(0,3),(0,4)]) 


    def test_calc_inner_template_size_9(self):

        shape = (7, 11)
        pos = (-4, -1)
        size = (6, 6)

        pos_val = (0, 0)
        size_val = (4, 5)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(4,0),(1,0)]) 

    def test_calc_inner_template_size_10(self):

        shape = (7, 11)
        pos = (6, 7)
        size = (4, 3)

        pos_val = (4, 7)
        size_val = (3, 3)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (2,0))
        self.assertEqual(pd, [(0,3),(0,0)]) 



    def test_calc_inner_template_size_11(self):

        shape = (7, 11)
        pos = (2, 2)
        size = (3, 4)

        pos_val = (2, 2)
        size_val = (3, 4)

        pos_out, size_out, pos_tpl, pd = \
                ds.calc_inner_template_size(shape, pos, size)

        print(pos_out)
        print(size_out)

        self.assertEqual(pos_out, pos_val)
        self.assertEqual(size_out, size_val)        
        self.assertEqual(pos_tpl, (0,0))
        self.assertEqual(pd, [(0,0),(0,0)])                 
                      
      
    def test_is_padding(self):
        self.assertTrue(ds.is_padding([(2,3),(0,0)]))
        self.assertTrue(ds.is_padding([(2,3),(20,3)]))
        self.assertTrue(ds.is_padding([(0,0),(3,0)]))
        self.assertFalse(ds.is_padding([(0,0),(0,0)]))

    def test_get_template_singlechannel_1(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        c = Tiffconnector(img_path,'path/to/nowhere/')
        
        c.filenames = [\
                ('6width4height3slices_rgb.tif', None)\
                , ('40width26height3slices_rgb.tif', None)\
                , ('40width26height6slices_rgb.tif', None)\
                ]
        
        d = Dataset(c)
        image_nr = 0
        pos = (0,0,0)
        size= (3, 6, 4)
        channel = 0
        tpl = d.get_template_singlechannel(image_nr, pos, size, channel, reflect=False)

        
        self.assertEqual(tpl.shape,(3,6,4))


    def test_get_template_singlechannel_2(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        c = Tiffconnector(img_path,'path/to/nowhere/')
        
        c.filenames = [\
                ('6width4height3slices_rgb.tif', None)\
                , ('40width26height3slices_rgb.tif', None)\
                , ('40width26height6slices_rgb.tif', None)\
                ]
        
        d = Dataset(c)
        image_nr = 0
        pos = (0,0,0)
        size= (1, 6, 4)
        channel = 0
        tpl = d.get_template_singlechannel(image_nr, pos, size, channel, reflect=False)

        val = \
        [[[151, 132, 154, 190],\
           [140,  93, 122, 183],\
           [148, 120, 133, 171],\
           [165, 175, 166, 161],\
           [175, 200, 184, 161],\
           [174, 180, 168, 157]]]

        val = np.array(val) 
        print(val)
        print(tpl)      
        self.assertTrue((tpl == val).all())   


    def test_get_template_singlechannel_3(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        c = Tiffconnector(img_path,'path/to/nowhere/')
        
        c.filenames = [\
                ('6width4height3slices_rgb.tif', None)\
                , ('40width26height3slices_rgb.tif', None)\
                , ('40width26height6slices_rgb.tif', None)\
                ]
        
        d = Dataset(c)
        image_nr = 0
        pos = (0,-1,-2)
        size= (1, 3, 3)
        channel = 0
        tpl = d.get_template_singlechannel(image_nr, pos, size, channel, reflect=True)

        val = \
        [[[132, 151, 151],\
           [132,  151, 151],\
           [93, 140, 140]]]
        
        val = np.array(val) 
        print(val)
        print(tpl)   
        self.assertTrue((tpl == val).all())



    def test_get_template_singlechannel_4(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        c = Tiffconnector(img_path,'path/to/nowhere/')
        
        c.filenames = [\
                ('6width4height3slices_rgb.tif',  None)\
                , ('40width26height3slices_rgb.tif', None)\
                , ('40width26height6slices_rgb.tif', None)\
                ]
        
        d = Dataset(c)
        image_nr = 0
        pos = (0, 4, 2)
        size= (1, 2, 6)
        channel = 0
        tpl = d.get_template_singlechannel(image_nr, pos, size, channel, reflect=True)

        val = \
        [[[184, 161, 161, 184, 200, 175],\
           [168,  157, 157, 168, 180, 174]]]
        
        val = np.array(val) 
        print(val)
        print(tpl)   
        self.assertTrue((tpl == val).all())


    def test_label_coordinates_to_5d(self):

        label_dict = \
            {
            2 : [(1, 3, 0, 0), (1, 5, 1, 2)],
            3 : [(1, 3, 1, 2), (1, 5, 3, 4), (1,1,1,1)],
            }

        image_nr = 2

        val = \
            {
            2 : [(2, 1, 3, 0, 0), (2, 1, 5, 1, 2)],
            3 : [(2, 1, 3, 1, 2), (2, 1, 5, 3, 4), (2, 1,1,1,1)],
            }
        
        out = ds.label_coordinates_to_5d(label_dict, image_nr)

        self.assertEqual(val, out)
      
            
        

    def test_label_coordinates_is_valid(self):
        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ('6width4height3slices_rgb.tif', None)\
                , ('40width26height3slices_rgb.tif', None)\
                , ('40width26height6slices_rgb.tif', None)\
                ]
        
        d = Dataset(c)

        #duplicate
        coor = \
            {
            2 : [(2, 0, 3, 0, 0), (2, 0, 5, 1, 2)],
            3 : [(2, 0, 3, 1, 2), (2, 0, 5, 3, 4), (2, 0,1,1,1), (2, 0, 3, 0, 0)],
            }


        self.assertFalse(d.label_coordinates_is_valid(coor))

        # one tuple with 4 instead 5 coordinate dimensions
        coor = \
            {
            2 : [(2, 0, 3, 0, 0), (2, 0, 5, 1, 2)],
            3 : [(2, 0, 3, 1, 2), (2, 0, 5, 3), (2, 0,1,1,1)],
            }


        self.assertFalse(d.label_coordinates_is_valid(coor))  

        # image nr too high
        coor = \
            {
            2 : [(2, 0, 3, 0, 0), (2, 0, 5, 1, 2)],
            3 : [(2, 0, 3, 1, 2), (3, 0,1,1,1)],
            }


        self.assertFalse(d.label_coordinates_is_valid(coor))     


        # out of image bounds
        coor = \
            {
            2 : [(0, 0, 3, 7, 4), (0, 0, 3, 1, 2)]
            }

        self.assertFalse(d.label_coordinates_is_valid(coor))

        # out of image bounds
        coor = \
            {
            2 : [(0, 0, -1, 6, 4), (0, 0, 3, 1, 2)]
            }

        self.assertFalse(d.label_coordinates_is_valid(coor))

        # out of image bounds
        coor = \
            {
            2 : [(0, 2, 0, 6, 4), (0, 1, 3, 1, 2)]
            }

        self.assertFalse(d.label_coordinates_is_valid(coor))

        # correct
        coor = \
            {
            2 : [(0, 0, 0, 6, 4), (0, 0, 3, 1, 2)]
            }

        self.assertTrue(d.label_coordinates_is_valid(coor))         
  


    def test_load_label_coordinates(self):
        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()        

        val = \
            {
                91: [(2, 0, 0, 0, 0), (2, 0, 0, 3, 1), (2, 0, 0, 3, 2), (2, 0, 0, 4, 1)],
                109: [(0, 0, 0, 2, 1), (0, 0, 0, 2, 2), (0, 0, 0, 2, 3), (0, 0, 0, 3, 1), (0, 0, 0, 3, 2), (0, 0, 0, 3, 3), (0, 0, 1, 5, 0), (0, 0, 1, 5, 1), (0, 0, 2, 0, 0), (0, 0, 2, 1, 0), (0, 0, 2, 1, 2), (2, 0, 2, 9, 7), (2, 0, 2, 9, 8), (2, 0, 2, 12, 7)],
                150: [(0, 0, 0, 0, 1), (0, 0, 0, 4, 1), (0, 0, 0, 5, 1), (2, 0, 0, 2, 2), (2, 0, 1, 0, 2), (2, 0, 1, 39, 25)]
            }
        
        d = Dataset(c)
        d.load_label_coordinates()
        print(d.label_coordinates)

        self.assertEqual(val, d.label_coordinates)
    
    def test_get_weight_template_for_label(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        d.load_label_coordinates()

        img_nr = 0
        pos_czxy = (0,0,0)
        size_czxy = (1,6,4)
        label_value = 150
        mat = d._get_template_for_label_inner(img_nr,\
         pos_czxy, size_czxy, label_value)
        
        val = np.zeros(size_czxy)
        val[0,0,1] = 1
        val[0,4,1] = 1
        val[0,5,1] = 1 

        self.assertTrue((val==mat).all())


    def test_get_template_for_label_1(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        d.load_label_coordinates()

        img_nr = 0
        pos_czxy = (0,0,0)
        size_czxy = (1,6,4)
        label_value = 150
        mat = d.get_template_for_label(img_nr,\
         pos_czxy, size_czxy, label_value)
        
        val = np.zeros(size_czxy)
        val[0,0,1] = 1
        val[0,4,1] = 1
        val[0,5,1] = 1 

        self.assertTrue((val==mat).all())   


    def test_get_template_for_label_2(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        d.load_label_coordinates()

        img_nr = 0
        pos_czxy = (0,2,1)
        size_czxy = (1,7,2)
        label_value = 150
        mat = d.get_template_for_label(img_nr,\
         pos_czxy, size_czxy, label_value)
        
        val = np.zeros(size_czxy)
        # val[0,0,1] = 1
        # val[0,4,1] = 1
        # val[0,5,1] = 1 
        print(d.label_coordinates[150])
        print('tpl')
        print(mat)

        val = [\
            [0.,0.],\
            [0.,0.],\
            [1.,0.],\
            [1.,0.],\
            [1.,0.],\
            [1.,0.],\
            [0.,0.]\
        ]
        val = np.array(val)
        self.assertTrue((mat==val).all())         


    def test_get_weight_template_for_label_2(self):

        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        d.load_label_coordinates()
        d.set_weight_for_label(1.2, 150)
        img_nr = 0
        pos_czxy = (0,0,0)
        size_czxy = (1,6,4)
        label_value = 150
        mat = d._get_template_for_label_inner(img_nr,\
         pos_czxy, size_czxy, label_value)
        
        val = np.zeros(size_czxy)
        print('valshae')
        print(val.shape)
        val[0,0,1] = 1.2
        val[0,4,1] = 1.2
        val[0,5,1] = 1.2 

        self.assertTrue((val==mat).all())    



    def test_load_label_coordinates(self):
        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        d.load_label_coordinates()
        d.init_label_weights()

        print(d.label_weights)
        print(d.label_coordinates)
        #check if dimensions match
        self.assertEqual(d.label_weights.keys(), d.label_coordinates.keys())
        self.assertEqual(len(d.label_weights[91]), len(d.label_coordinates[91]))
        self.assertEqual(len(d.label_weights[109]), len(d.label_coordinates[109]))
        self.assertEqual(len(d.label_weights[150]), len(d.label_coordinates[150]))
        
        self.assertEqual(set(d.label_weights[91]), set([1]))    
        self.assertEqual(set(d.label_weights[109]), set([1]))    
        self.assertEqual(set(d.label_weights[150]), set([1]))    

    
    def test_set_weight_for_label(self):
        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        
        d.set_weight_for_label(0.7, 150)

        self.assertEqual(d.label_weights[150], [0.7, 0.7, 0.7, 0.7, 0.7, 0.7])
        self.assertEqual(d.label_weights[91], [1, 1, 1, 1])

    def test_equalize_label_weights(self):
        img_path = os.path.join(base_path, '../test_data/tiffconnector_1/im/')
        label_path = os.path.join(base_path, '../test_data/tiffconnector_1/labels/')
        c = Tiffconnector(img_path,label_path)
        
        c.filenames = [\
                ['6width4height3slices_rgb.tif', '6width4height3slices_rgb.tif']\
                , ['40width26height6slices_rgb.tif', None]\
                , ['40width26height3slices_rgb.tif', '40width26height3slices_rgb.tif']\
                ]
        c.load_label_filenames()    

        d = Dataset(c)
        
        d.equalize_label_weights()

        print(d.label_weights)

        res = np.unique(np.array(d.label_weights[91])) + \
            np.unique(np.array(d.label_weights[109])) + \
            np.unique(np.array(d.label_weights[150])) 
        
        print(res)
        self.assertEqual(np.round(res[0],3), 1.)

            

    def test_label_to_mask(self):
        shape = (5,4)
        pos = (2,1)
        size = (3,2)
        label_coors = [(0,0), (2,1), (2,2)]
        weights = [2, 2, 2]
        mat = ds.label2mask(shape, pos, size, label_coors, weights)    
        val = \
            [[2., 2.],\
            [0., 0.],\
            [0., 0.]]

        val = np.array(val)    


        print(mat)
        self.assertTrue((val == mat).all())


    def test_weights_to_mask(self):
        shape = (5,4)
        pos = (2,1)
        size = (3,2)
        label_coors = [(0,0), (2,1), (2,2)]
        weights = [1, 2, 3]
        
        mat = ds.label2mask(shape, pos, size, label_coors, weights)    
        val = \
            [[2., 3.],\
            [0., 0.],\
            [0., 0.]]

        val = np.array(val)    


        print(mat)
        self.assertTrue((val == mat).all())    

    def test_calc_equalized_label_weights(self):
        
        label_n = {1: 10, 2 : 20}

        weights = ds.calc_equalized_label_weights(label_n)

        print(weights)
        self.assertEqual(weights[1]/2, weights[2])
        self.assertEqual(weights[1]+weights[2], 1)

    # def test_get_augmented_template(self):
        
    #     def get_tpl_func(pos=None, size=None, img=None):
    #         return img[get_template_meshgrid(img.shape, pos, size)]


    #     im = np.zeros((7,5))
    #     im[3,:] = 1
    #     im[3,2] = 2

    #     pos = (2,1)
    #     size=(3,3)
        

    #     tpl = get_tpl_func(pos=pos, size=size, img=im)

    #     tpl_rot = ds.get_augmented_template(im.shape, pos, size, \
    #     get_tpl_func, rotation_angle=0, shear_angle=0, **{'img': im})

    #     print(im)
    #     print(tpl)
    #     print(tpl_rot)

    #     self.assertTrue(False)



