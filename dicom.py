from walkdir import filtered_walk, file_paths
import pydicom
import os
import numpy as np
import matplotlib.pyplot as plt

def get_images_from_dir(dicom_dir_path):
    pixel_arrays = []
    dicom_file_paths = file_paths(filtered_walk(dicom_dir_path, included_files=["*.dcm"]))
    for dicom_file_path in dicom_file_paths:
        pixel_arrays.append(pydicom.read_file(dicom_file_path).pixel_array)
        
    return pixel_arrays

# max
def get_MIP(pixel_arrays):
    result = np.zeros_like(pixel_arrays[0])
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            for array in range(len(pixel_arrays)):
                result[row][col] = max([result[row][col], pixel_arrays[array][row][col]])
    
    return result
    

#min
def get_mIP(pixel_arrays):
    result = np.array(pixel_arrays[0])
    result.fill(100000)
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            for array in range(len(pixel_arrays)):
                result[row][col] = min([result[row][col], pixel_arrays[array][row][col]])
    
    return result


#avg
def get_AIP(pixel_arrays):
    result = np.zeros_like(pixel_arrays[0])
    for row in range(result.shape[0]):
        for col in range(result.shape[1]):
            items = []
            for array in range(len(pixel_arrays)):
                items.append(pixel_arrays[array][row][col])
            result[row][col] = np.average(items)
    
    return result


def get_function_by_mode(mode):
    if mode == 'MIP':
        return get_MIP
    elif mode == 'mIP':
        return get_mIP
    else:
        return get_AIP

def save_image_with_mode(pixel_arrays, mode, result_file_name):
    pixel_array = get_function_by_mode(mode)(pixel_arrays)
    plt.axis('off')
    plt.imshow(pixel_array, cmap=plt.cm.gray)
    plt.savefig(result_file_name)


#save_image_with_mode(get_images_from_dir('./img/'), 'MIP', 'MIP.png')
save_image_with_mode(get_images_from_dir('./img/'), 'mIP', 'mIP.png')
#save_image_with_mode(get_images_from_dir('./img/'), 'AIP', 'AIP.png')
