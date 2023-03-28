import SimpleITK as sitk
import numpy as np
from PIL import Image
import os

def load_itk(filename):
    # Reads the image using SimpleITK
    itkimage = sitk.ReadImage(filename)

    # Convert the image to a numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(itkimage)

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))

    return ct_scan, origin, spacing

input_dir = 'data/luna16/images/subset2'
output_dir = 'data/luna16/images/jpg/subset2'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.mhd'):
        # Load the image using SimpleITK
        full_path = os.path.join(input_dir, filename)
        ct_scan, _, _ = load_itk(full_path)

        # Convert the image to a PIL image object
        ct_scan_uint8 = ct_scan.astype(np.uint8)
        image = Image.fromarray(ct_scan_uint8[0])

        # Save the image in JPEG format
        base_filename = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, base_filename + '.jpg')
        image.save(output_path)
