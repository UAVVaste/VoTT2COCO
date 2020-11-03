# VoTT2COCO
Script that converts [VoTT](https://github.com/microsoft/VoTT) json files to [COCO](https://cocodataset.org/#home) format. Keeps images, bboxes, and masks.

# Usage

### Modify/create yaml file
``` yaml
dataset:
  source:
    path: '/home/bartosz/UAVVaste_vott/'   ### main catalog
    img_cat: images                        ### name of sub-catalogs with images
    anno_cat: annotations                  ### name of sub-catalog with annotations jsons
  destination:
    path: '/home/bartosz/UAVVaste_coco/'
    img_cat: images
    anno_file: annotations.json

info:
  year: 2020 
  version: v1 
  description: UAVVaste dataset 
  contributor: None
  url: https://uavvaste.ithub.io/
```

### Run script
``` bash
python vott2coco.py -c conver_config.yml
```
