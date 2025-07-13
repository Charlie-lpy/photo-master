import argparse
from pathlib import Path

from src.parse_excel import load_excel, extract_profile_data
from src.downloader import download_photos
from src.validator import validate_photos_in_folder, save_validation_results
from src.cropper import crop_photos_in_folder
from src.size_adjuster import resize_photos_in_folder

def parse_args():
    parser = argparse.ArgumentParser(description="🖼️ Profile Photo Processing Tool: Download, Validate, Crop, Resize")
    
    parser.add_argument("--tool", choices=["download", "validate", "crop", "resize", "all"], default="all",
                        help="Which tool to use: download, validate, crop, resize, or all (default: all)")

    # Download
    parser.add_argument("--download_input_report", type=str, default="data/raw_reports/demo_profile_photo_report2.xlsx",
                        help="Path to Excel input file")
    parser.add_argument("--download_input_sheet", type=str, default="Sheet1", help="Name of the Excel sheet (default: Sheet1)")
    parser.add_argument("--download_photo_folder", type=str, default="photos/downloaded",
                        help="Folder to save downloaded photos")

    # Validation
    parser.add_argument("--validate_input_photo_folder", type=str, default="photos/downloaded",
                        help="Folder containing photos to validate")
    parser.add_argument("--validate_output_report", type=str, default="data/output_reports/photo_validation_results.xlsx",
                        help="Path to save the validation report Excel file")

    # Crop
    parser.add_argument("--crop_input_photo_folder", type=str, default="photos/demo_raw")
    parser.add_argument("--crop_output_photo_folder", type=str, default="photos/demo_cropped",
                        help="Folder to save cropped photos")

    # Resize
    parser.add_argument("--resize_input_photo_folder", type=str, default="photos/demo_cropped")
    parser.add_argument("--resize_output_photo_folder", type=str, default="photos/demo_resized",
                        help="Folder to save resized photos")

    return parser.parse_args()

def main():
    args = parse_args()

    # Resolve paths
    download_input_report_path = Path(args.download_input_report)
    download_photo_folder = Path(args.download_photo_folder)
    validate_input_photo_folder = Path(args.validate_input_photo_folder)
    validate_output_report_path = Path(args.validate_output_report)
    crop_input_photo_folder = Path(args.crop_input_photo_folder)
    crop_output_photo_folder = Path(args.crop_output_photo_folder)
    resize_input_photo_folder = Path(args.resize_input_photo_folder)
    resize_output_photo_folder = Path(args.resize_output_photo_folder)

    df = None
    profile_records = None

    # === Tool 1: Download Photos + Validation ===
    if args.tool in ["download", "all"]:
        df = load_excel(download_input_report_path, sheet_name=args.download_input_sheet)
        if df is None:
            print("❌ Failed to load Excel file. Exiting.")
            return

        profile_records = extract_profile_data(
            df,
            id_col="Confirmation_Number",
            url_col="Image_URL",
            photoname_col="Photo_Name",
        )

        print(f"⬇️ Downloading {len(profile_records)} photos...")
        error_list = download_photos(profile_records, output_folder=download_photo_folder, sleep_time=0.2)
        if error_list:
            print(f"⚠️ {len(error_list)} photo downloads failed.")
            print(f"Failed downloads: {error_list}")
        else:
            print("✅ All photos downloaded successfully.")

        print("🔍 Validating the downloaded photos...")
        validation_results = validate_photos_in_folder(download_photo_folder)
        save_validation_results(validation_results, validate_output_report_path, merge_original_df=df, left_on="Photo_Name", right_on="Photo_Name")

    # === Tool 2: Validate Only ===
    if args.tool == "validate":
        print("🔍 Validating photos...")
        validation_results = validate_photos_in_folder(validate_input_photo_folder)
        save_validation_results(validation_results, validate_output_report_path)

    # === Tool 3: Crop Photos ===
    if args.tool in ["crop", "all"]:
        print("✂️ Cropping photos...")
        crop_photos_in_folder(crop_input_photo_folder, crop_output_photo_folder)
        print(f"✅ Cropped photos saved to {crop_output_photo_folder}")

    # === Tool 4: Resize Photos ===
    if args.tool in ["resize", "all"]:
        print("📏 Resizing photos...")
        resize_photos_in_folder(resize_input_photo_folder, resize_output_photo_folder)
        print(f"✅ Resized photos saved to {resize_output_photo_folder}")

if __name__ == "__main__":
    main()
