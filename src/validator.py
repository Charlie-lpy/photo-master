import os
from PIL import Image
import pandas as pd

def validate_photo(photo_path):
    """
    Validate a single photo by checking its size, dimensions, and aspect ratio.
    Returns a dictionary with the results or None if validation fails.
    """
    try:
        with Image.open(photo_path) as img:
            photoname = os.path.splitext(os.path.basename(photo_path))[0]
            file_size_kb = os.path.getsize(photo_path) / 1024  # in KB
            width = img.size[0]
            height = img.size[1]
            ratio = width / height if height != 0 else None

            result_dict = {
                'Photo_Name': photoname,
                'file_size_kb': file_size_kb,
                'width': width,
                'height': height,
                'ratio': ratio,
            }
        
        return result_dict

    except Exception as e:
        print(f"❌ Error while processing {photo_path}: {e}")
        return None

def validate_photos_in_folder(folder_path):
    """
    Validate all photos in a given folder.
    Returns a list of dictionaries with validation results for each photo.
    """
    result_dict_list = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            photo_path = os.path.join(folder_path, filename)
            result_dict = validate_photo(photo_path)
            if result_dict:
                result_dict_list.append(result_dict)
    return result_dict_list

def save_validation_results(results, output_path, merge_original_df=None, left_on='Photo_Name', right_on='Photo_Name'):
    """
    Save validation results to an Excel file.
    If merge_original_df is provided, merge it with the validation results on merge_on column.
    :param results: List of dictionaries with validation results
    :param output_path: Path to save the Excel file
    :param merge_original_df: DataFrame to merge with validation results (optional)
    :param left_on: Column name in merge_original_df to merge on
    :param right_on: Column name in results to merge on
    """
    df = pd.DataFrame(results)
    
    # Make sure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        if merge_original_df is not None:
            df = pd.merge(merge_original_df, df, how='left', left_on=left_on, right_on=right_on)
        df.to_excel(output_path, index=False)
        print(f"✅ Validation results saved to {output_path}")
    except Exception as e:
        print(f"❌ Failed to save validation results: {e}")
