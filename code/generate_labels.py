import pandas as pd
import os

classes = ['nodule']

df = pd.read_csv('data/luna16/annotations/annotations.csv')
for _, row in df.iterrows():
    image_name = row['seriesuid'] + '.mhd'
    label = row['diameter_mm']
    x, y, z = row['coordX'], row['coordY'], row['coordZ']

    x_min, y_min, z_min = x - label/2, y - label/2, z - label/2
    x_max, y_max, z_max = x + label/2, y + label/2, z + label/2

    with open(f'data/yolo/labels/{image_name[:-4]}.txt', 'a') as f:
        f.write(f"{classes.index('nodule')} {(x_min+x_max)/2} {(y_min+y_max)/2} {(z_min+z_max)/2} {x_max-x_min} {y_max-y_min} {z_max-z_min}\n")

