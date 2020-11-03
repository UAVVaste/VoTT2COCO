import json
from tqdm import tqdm
import cv2
import numpy as np
import os
from glob import glob

class VOTItem:
    def __init__(self, path, index, img_dir):
        self.item_dict = json.load(open(path, 'r'))

        self.index = index
        self.width = self.item_dict['asset']['size']['width']
        self.height = self.item_dict['asset']['size']['height']
        self.name = self.item_dict['asset']['name']

        self.bbox, self.categories = self.__read_bboxes()
        self.masks, self.areas = self.__read_masks()

        self.image_path = path.split('annotations')[0] + \
            f'{img_dir}/{self.name}'

    def __read_bboxes(self):
        bboxes_list = []
        categories_list = []

        for data in self.item_dict['regions']:
            bboxes_list.append([
                int(data['boundingBox']['left']),
                int(data['boundingBox']['top']),
                int(data['boundingBox']['width']),
                int(data['boundingBox']['height']),
            ])

            categories_list.append(data['tags'][0])

        return bboxes_list, categories_list
    
    def __read_masks(self):
        masks_list = []
        areas = []

        for data in self.item_dict['regions']:
            mask = []
            area = 0

            for point in data['points']:
                mask.append(int(point['x']))
                mask.append(int(point['y']))

            masks_list.append([mask])
            areas.append(cv2.contourArea(np.array([
                [[mask[i], mask[i+1]] for i in range(0, len(mask), 2)]
            ])))
        

        return masks_list, areas

class VOTTReader:
    def __init__(self, config):
        self.config = config
        self.global_index = 0
        self.categories = []
        self.items = []

    def parse_files(self):
        directory = self.config['dataset']['source']['path']
        key = self.config['dataset']['source']['anno_cat']
        img_dir = self.config['dataset']['source']['img_cat']
        files_list = glob(f'{directory}**/{key}/*.json')

        print(f'[LOGS] Parsing {len(files_list)} VoTT json files')
        for path in tqdm(files_list):
            item = VOTItem(path, self.global_index, img_dir)

            for cat in set(item.categories):
                if cat not in self.categories:
                    self.categories.append(cat) 

            self.global_index += 1
            self.items.append(item)