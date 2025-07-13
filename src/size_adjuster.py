import os
import io
from PIL import Image, ImageOps

def resize_photo(img, output_path, min_kb=50, max_kb=1024):
    """
    Adjust the size of a photo to fall within the specified size range.
    Returns True if adjustment was successful, False otherwise.
    """

    def get_buffer_size(image, quality=100):
        buffer = io.BytesIO()
        image.save(buffer, quality=quality, format='JPEG')
        return len(buffer.getvalue()) / 1024, buffer

    basename = os.path.basename(output_path)
    quality = 100
    size_kb, buffer = get_buffer_size(img, quality)

    if size_kb < min_kb:
        print(f"⚠️ {basename}: Too SMALL at {size_kb:.2f} KB (quality {quality}).")
        return False

    elif size_kb > max_kb:
        while size_kb > max_kb and quality > 4:
            quality -= 5
            size_kb, buffer = get_buffer_size(img, quality)
        if size_kb > max_kb:
            print(f"⚠️ {basename}: Too Big at quality {quality}.")
            return False

    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())
    return True


def resize_photos_in_folder(input_folder, output_folder, min_kb=50, max_kb=1024):
    """
    Process all images in a folder and adjust their sizes to be within the target range.
    """
    os.makedirs(output_folder, exist_ok=True)
    fail_subfolder = os.path.join(output_folder, "failed")
    os.makedirs(fail_subfolder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue  # skip non-image files

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            original_size_kb = os.path.getsize(input_path) / 1024

            with Image.open(input_path) as img:
                img = ImageOps.exif_transpose(img)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                if min_kb <= original_size_kb <= max_kb:
                    img.save(output_path, format='JPEG')
                else:
                    success = resize_photo(img, output_path, min_kb, max_kb)
                    if not success:
                        fail_path = os.path.join(fail_subfolder, filename)
                        img.save(fail_path, format='JPEG')
        

        except Exception as e:
            print(f"💥 {filename}: Error during processing — {e}")

    fail_num = len(os.listdir(fail_subfolder))
    if fail_num > 0:
        print(f"⚠️ {fail_num} photos failed to resize and were moved to '{fail_subfolder}'.")
    else:
        print("✅ All photos resized successfully.")
