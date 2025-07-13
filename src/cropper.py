import os
from PIL import Image, ImageOps

def crop_to_aspect_ratio(image, target_ratio=0.75):
    """
    Crop the image to the desired aspect ratio (e.g. 0.75 = 3:4).
    Center crop only. Returns a new cropped image.
    """
    width, height = image.size
    current_ratio = width / height

    if abs(current_ratio - target_ratio) < 0.01:
        return image  # already close enough, no cropping

    if current_ratio > target_ratio:
        # too wide → crop width
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        box = (left, 0, left + new_width, height)
    else:
        # too tall → crop height
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        box = (0, top, width, top + new_height)

    return image.crop(box)

def crop_photos_in_folder(input_folder, output_folder, target_ratio=0.75):
    """
    Crop all images in input_folder to the target aspect ratio.
    Save results in output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png')

    print(f"📂 Cropping photos in {input_folder} to aspect ratio {target_ratio}...")
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(SUPPORTED_EXTS):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                with Image.open(input_path) as img:
                    img = ImageOps.exif_transpose(img)
                    cropped_img = crop_to_aspect_ratio(img, target_ratio)

                    # 🔥 Convert RGBA → RGB if needed
                    if cropped_img.mode == 'RGBA':
                        cropped_img = cropped_img.convert('RGB')
                    cropped_img.save(output_path)

            except Exception as e:
                print(f"❌ Failed to crop {filename}: {e}")
