import SimpleITK as sitk
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt

def load_itk_image(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    return numpyImage, numpyOrigin, numpySpacing

def readCSV(filename):
    lines = []
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines

def worldToVoxelCoord(worldCoord, origin, spacing):
    stretchedVoxelCoord = np.absolute(worldCoord - origin)
    voxelCoord = stretchedVoxelCoord / spacing
    return voxelCoord

def normalizePlanes(npzarray):
    maxHU = 400.
    minHU = -1000.

    npzarray = (npzarray - minHU) / (maxHU - minHU)
    npzarray[npzarray > 1] = 1.
    npzarray[npzarray < 0] = 0.
    return npzarray

img_path = 'data/luna16/images/subset0/1.3.6.1.4.1.14519.5.2.1.6279.6001.105756658031515062000744821260.mhd'
cand_path = 'data/luna16/csv/candidates.csv'

numpyImage, numpyOrigin, numpySpacing = load_itk_image(img_path)
cands = readCSV(cand_path)

# mark nodules on the image
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(numpyImage[0], cmap='gray')
for i, cand in enumerate(cands[1:]):
    # extract the nodule coordinates
    worldCoord = np.asarray([float(cand[3]),float(cand[2]),float(cand[1])])
    voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
    voxelWidth = 65
    
    # draw a circle around the nodule
    diameter = float(cand[4])
    radius = voxelWidth / 2
    circle = plt.Circle((voxelCoord[1], voxelCoord[2]), radius, color='r', fill=True, alpha=0.3)
    ax.add_artist(circle)
    ax.annotate(f"{diameter:.1f} mm", (voxelCoord[1]-radius, voxelCoord[2]-radius), color='r', fontsize=8)

# Save the marked image
outputDir = 'data/luna16/marked_images/'
imageName = os.path.splitext(os.path.basename(img_path))[0] + '.jpg'
outputPath = os.path.join(outputDir, imageName)
plt.savefig(outputPath)

