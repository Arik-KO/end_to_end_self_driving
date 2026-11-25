from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image
from nuscenes.nuscenes import NuScenes


DATAROOT = "data/nuscenes-mini"
VERSION = "v1.0-mini"
SCENE_INDEX = 0
SAMPLE_INDEX = 0


CAMERA_GRID = [
    ["CAM_FRONT_LEFT", "CAM_FRONT", "CAM_FRONT_RIGHT"],
    ["CAM_BACK_LEFT", "CAM_BACK", "CAM_BACK_RIGHT"],
]


nusc = NuScenes(version = VERSION, dataroot=str(DATAROOT), verbose = True)  # this is an object from nusc class which is designed by nuscenes-devkit repo

"""
This is not a typical docstring. Just writing notes from my finidigs.
while loading verbose=True can let us know about the tables. The name of tables and its element will be printed.
we can check the type of those tables. From the print statements below are giving me the information about them. 
For example, scene and sample are lists. 
"""

first_sample = nusc.sample[SAMPLE_INDEX]
first_scene = nusc.scene[SCENE_INDEX]
annos = len(first_sample["anns"])

# Need to investigate how many samples per token
last_sample_token = first_scene["last_sample_token"]
for sample in range(len(nusc.sample)):
    if nusc.sample[sample]["token"] == last_sample_token:
        print(sample)
        break
# for the first scene the last sample is found for sample number 38+1. Since total sample is 404, I guess it is going to vary for each scene.
# why for first scene the total anns from the first sample was 69? = Number of objects in a scene and for each object annotations are done.

# checking how nusc.get works

last_sample_element = nusc.get("sample", last_sample_token)
second_sample_element = nusc.get("sample", first_sample['next'])
#print(second_sample_element)

for row in CAMERA_GRID:
    for camera_name in row:
        camera_token = last_sample_element["data"][camera_name]
        sample_record = nusc.get("sample_data", camera_token)
        offset = (sample_record["timestamp"] - last_sample_element["timestamp"]) / 1000
        print(f"{camera_name:<18} {offset:+8.1f} {sample_record['filename']}")

#print(nusc.sample_data[0].keys())
#print(nusc.sample_data[0])

fig, axes = plt.subplots(2,3, figsize=(18, 7))
for row in range(2):
    for col in range(3):
        camera_name = CAMERA_GRID[row][col]
        camera_token = second_sample_element["data"][camera_name]
        image_path = nusc.get_sample_data_path(camera_token)   #this method probably given in the doc string found by help(nusc)
        image = Image.open(image_path)

        print(image.size)
        ax = axes[row,col]
        ax.imshow(image)
        ax.set_title(camera_name)
        ax.axis("off")


plt.tight_layout()
plt.show()

#print(type(nusc))
#print(help(nusc))
#print(nusc.list_scenes())
#print(type(nusc.scene))
#print(type(nusc.sample))
#print("total scenes it should match with verbose information",len(nusc.scene))
#print("total samples it should match with verbose information", len(nusc.sample))
#print(nusc.scene[0]) # checking scenes since it is a list all 10 scenes info are here
#print()
#print(nusc.sample[0]) # doing same for sample
#print(annos)
#print(nusc.sample[1])
#print(first_scene.keys()) # -> this line demonstrates link to other tables
