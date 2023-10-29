# Importing required libraries
import os
from PIL import Image
import numpy as np
import pandas as pd

# Function to get all subdirectories
def get_subdirs(top_dir):
    return [os.path.join(top_dir, d) for d in os.listdir(top_dir) if os.path.isdir(os.path.join(top_dir, d))]

# Function to read a .tif file and return as numpy array
def read_tif_file(file_path):
    try:
        with Image.open(file_path) as img:
            return np.array(img)
    except Exception as e:
        log_error(f"Error reading {file_path}: {e}")
        return None

# Function to calculate average intensity of an image
def calculate_avg_intensity(image_array):
    return np.mean(image_array)

# Function to calculate the percentage of pixels that are positive based on a cutoff
def calculate_percent_positive(image_array, cutoff):
    positive_pixels = np.sum(image_array > cutoff)
    total_pixels = image_array.size
    return (positive_pixels / total_pixels) * 100

# Function to calculate single and double positives
def calculate_single_and_double_positives(image1, image2, cutoff):
    single_positive1 = np.sum((image1 > cutoff) & (image2 <= cutoff))
    single_positive2 = np.sum((image1 <= cutoff) & (image2 > cutoff))
    double_positive = np.sum((image1 > cutoff) & (image2 > cutoff))
   
    total_pixels = image1.size  # assuming both images are of the same size
   
    return (single_positive1 / total_pixels) * 100, (single_positive2 / total_pixels) * 100, (double_positive / total_pixels) * 100

# Function to log errors for debugging
def log_error(message):
    print(f"Error: {message}")

# Main function to iterate through each sub-directory and perform analyses
# Modified main function to add NAs for missing or unreadable .tif files
def main(top_dir):
    # Initialize an empty DataFrame
    df = pd.DataFrame(columns=['Sub-dir', 'Saa3_avg_intensity', 'Cxcl10_avg_intensity',
                               'Saa3_percent_positive', 'Cxcl10_percent_positive',
                               'Saa3_single_positive', 'Cxcl10_single_positive', 'Double_positive'])
   
    # Iterate through each sub-directory
    for sub_dir in get_subdirs(top_dir):
        # Initialize a dictionary to hold the results for this sub-directory
        results = {'Sub-dir': os.path.basename(sub_dir)}
       
        # Read the .tif files
        saa3_image = read_tif_file(os.path.join(sub_dir, "Saa3.tif"))
        cxcl10_image = read_tif_file(os.path.join(sub_dir, "Cxcl10.tif"))
       
        if saa3_image is None:
            results.update({
                'Saa3_avg_intensity': 'NA',
                'Saa3_percent_positive': 'NA',
                'Saa3_single_positive': 'NA'
            })
       
        if cxcl10_image is None:
            results.update({
                'Cxcl10_avg_intensity': 'NA',
                'Cxcl10_percent_positive': 'NA',
                'Cxcl10_single_positive': 'NA'
            })
       
        # If both images are missing or unreadable, also set Double_positive to 'NA'
        if saa3_image is None and cxcl10_image is None:
            results['Double_positive'] = 'NA'
       
        # Calculate metrics for saa3_image if it's available
        if saa3_image is not None:
            results['Saa3_avg_intensity'] = calculate_avg_intensity(saa3_image)
            results['Saa3_percent_positive'] = calculate_percent_positive(saa3_image, 4000)
       
        # Calculate metrics for cxcl10_image if it's available
        if cxcl10_image is not None:
            results['Cxcl10_avg_intensity'] = calculate_avg_intensity(cxcl10_image)
            results['Cxcl10_percent_positive'] = calculate_percent_positive(cxcl10_image, 4000)
       
        # Calculate single and double positives if both images are available
        if saa3_image is not None and cxcl10_image is not None:
            saa3_single, cxcl10_single, double_positive = calculate_single_and_double_positives(saa3_image, cxcl10_image, 4000)
            results['Saa3_single_positive'] = saa3_single
            results['Cxcl10_single_positive'] = cxcl10_single
            results['Double_positive'] = double_positive
       
        # Append results to DataFrame
        df = df.append(results, ignore_index=True)
   
    return df

top_dir = "/media/scott/Seagate Backup Plus Drive/jordi/processed_images"
df = main(top_dir)
df.to_csv(os.path.join(os.path.dirname(top_dir),"image_data_analysis.tsv"), sep="\t")

