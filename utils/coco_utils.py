import json
from datetime import datetime
from tqdm import tqdm
from shutil import copyfile
from pathlib import Path



class COCOSaver:
    def __init__(self, config, reader):
        self.config = config
        self.reader = reader

        self.cat_dict = {}
        self.anno_global_index = 0

        self.info = self.__create_info()
        self.categories = self.__create_categories()

        self.coco = {
            'images': [],
            'categories': self.categories,
            'annotations': [],
            'licenses': [],
            'info': self.info
        }

    def save(self):
        directory = self.config['dataset']['destination']['path']
        key = self.config['dataset']['destination']['img_cat']

        img_path = Path(f'{directory}{key}')
        img_path.mkdir(parents=True, exist_ok=True)

        for item in tqdm(self.reader.items):
            self.coco['images'].append(self.__create_image(item.index, item.width, item.height, item.name))
            copyfile(item.image_path, f'{str(img_path)}/{item.name}')

            self.coco['annotations'] += self.__create_annotations(item.index, item.bbox, item.masks, item.areas, item.categories)

        json.dump(self.coco, open(directory+self.config['dataset']['destination']['anno_file'], 'w'))


    def __create_info(self):
        info = {
            'year': self.config['info']['year'], 
            'version': self.config['info']['version'], 
            'description': self.config['info']['description'], 
            'contributor': self.config['info']['contributor'], 
            'url': self.config['info']['url'], 
            'date_created': str(datetime.now())
        }

        return info

    def __create_categories(self):
        categories = []
        for i, name in enumerate(sorted(self.reader.categories)):
            categories.append(
                {
                'supercategory': '', 
                'id': i, 
                'name': name
                }
            )

            self.cat_dict[name] = i
        
        return categories

    def __create_image(self, id, width, height, file_name):
        return {
            'id': id, 
            'width': width, 
            'height': height, 
            'file_name': file_name, 
            'license': None, 
            'flickr_url': None, 
            'coco_url': None, 
            'date_captured': None, 
            'flickr_640_url': None
        }

    def __create_annotations(self, id, bboxs, masks, areas, categories):
        annotations = []

        for bbox, mask, area, cat in zip(bboxs, masks, areas, categories):
            annotations.append(
                {
                    'id': self.anno_global_index, 
                    'image_id': id, 
                    'category_id': self.cat_dict[cat], 
                    'segmentation': mask,
                    'area': area, 
                    'bbox': bbox, 
                    'iscrowd': 0
                }
            )

            self.anno_global_index += 1

        return annotations