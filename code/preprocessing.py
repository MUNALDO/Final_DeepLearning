import numpy as np
import pandas as pd
import pydicom
import os
import SimpleITK as sitk

def load_scan(path):
    slices = sitk.ReadImage(path)
    image_array = sitk.GetArrayFromImage(slices)
    spacing = slices.GetSpacing()
    origin = slices.GetOrigin()
    return image_array, spacing, origin

def get_pixels_hu(scans):
    image = scans.astype(np.float32)
    image[image == -2000] = 0
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
    image += np.int16(intercept)
    return np.array(image, dtype=np.int16)

def preprocess(INPUT_FOLDER):
    patients = os.listdir(INPUT_FOLDER)
    for patient in patients:
        if '.mhd' in patient:
            patient_id = patient.split('.')[0]
            patient_path = os.path.join(INPUT_FOLDER, patient)
            print(f'Preprocessing patient {patient_id}')
            # load scan
            image_array, spacing, origin = load_scan(patient_path)
            # resample to 1mm pixel spacing
            new_spacing = [1, 1, 1]
            resize_factor = spacing / new_spacing
            new_real_shape = image_array.shape * resize_factor
            new_shape = np.round(new_real_shape)
            real_resize_factor = new_shape / image_array.shape
            new_spacing = spacing / real_resize_factor
            image_array = sitk.Resize(image_array, new_shape.astype(np.int), sitk.sitkLinear)
            # normalize pixel values
            image_array = get_pixels_hu(image_array)
            # save preprocessed image
            np.save(os.path.join(INPUT_FOLDER, f'{patient_id}.npy'), image_array)

if __name__ == '__main__':
    INPUT_FOLDER = 'data/luna16/images/subset0/'
    preprocess(INPUT_FOLDER)
