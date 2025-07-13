import pandas as pd

def load_excel(file_path, sheet_name="Sheet1"):
    """
    Load an Excel file and return a DataFrame.
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet to load.
    :return: DataFrame containing the data from the specified sheet.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
    
def extract_profile_data(df, id_col="Confirmation_Number", url_col="Image_URL", photoname_col="Photo_Name"):
    """
    Extract profile data from the DataFrame.
    :param df: DataFrame containing the profile data.
    :param id_col: Column name for the ID.
    :param url_col: Column name for the image URL.
    :param name_col: Column name for the profile name.
    :return: List of dictionaries with profile data.
    """
    profiles = []
    for index, row in df.iterrows():
        try:
            profile = {
                "id": row[id_col],
                "url": row[url_col],
                "photoname": row[photoname_col]
            }
            profiles.append(profile)
        except Exception as e:
            print(f"Skipping row {index} due to error: {e}")
            continue
    return profiles