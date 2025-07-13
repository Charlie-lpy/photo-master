import os
import requests
import time

def create_folder_if_not_exists(folder_path):
    """
    Create the folder if it doesn't exist.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def download_photos(profile_list, output_folder="photos/downloaded", sleep_time=0.3):
    """
    Download profile photos based on the provided profile data.
    :param profile_list: List of dictionaries with 'url' and 'photoname' keys
    :param output_folder: Folder to save the downloaded photos
    :param sleep_time: Time to sleep between requests to avoid overwhelming the server
    :return: List of profiles that failed to download
    """
    create_folder_if_not_exists(output_folder)

    error_list = []

    for profile in profile_list:
        url = profile["url"]
        photoname = profile["photoname"]
        id = profile["id"]

        time.sleep(sleep_time)  # Sleep to avoid overwhelming the server
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                output_path = os.path.join(output_folder, f"{photoname}.jpg")
                with open(output_path, "wb") as file:
                    file.write(response.content)

        except Exception as e:
            error_list.append(profile)
            print(f"Error downloading {photoname} (ID: {id}): {e}. URL: {url}")
            continue

    return error_list
    
