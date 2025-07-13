import streamlit as st
import os
import shutil
import zipfile
import pandas as pd
from PIL import Image
from src.parse_excel import load_excel, extract_profile_data
from src.downloader import download_photos
from src.validator import validate_photos_in_folder, save_validation_results
from src.cropper import crop_photos_in_folder
from src.size_adjuster import resize_photos_in_folder

st.set_page_config(page_title="Profile Photo Processor", page_icon="🖼️")
st.title("🖼️ Profile Photo Processing Tool")

# Set up directories
OUTPUT_DIR = "streamlit_output"
UPLOAD_DIR = "streamlit_uploaded"

tab1, tab2 = st.tabs(["📄 Excel Upload Workflow", "📁 Manual Image Upload"])

# === 📄 Tab 1: Excel Upload ===
with tab1:
    st.subheader("📄 Upload Excel and Run Full Pipeline")

    # ========== STEP 1: Upload Excel File ==========
    uploaded_excel = st.file_uploader("Upload Excel file with photo URLs", type=["xlsx"])
    if uploaded_excel:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        df = load_excel(uploaded_excel)
        st.success("Excel loaded!")
        st.dataframe(df.head())

        # ========== STEP 2: Choose Processing Steps ==========
        steps = st.multiselect(
            "🛠️ Choose processing steps",
            ["Download", "Crop", "Resize", "Validate"],
            default=["Download", "Crop", "Resize", "Validate"]
        )

        if st.button("🚀 Run Selected Steps"):
            profiles = extract_profile_data(
                df, 
                id_col="Confirmation_Number", 
                url_col="Image_URL", 
                photoname_col="Photo_Name"
            )
            
            downloaded_dir = os.path.join(OUTPUT_DIR, "downloaded")
            cropped_dir = os.path.join(OUTPUT_DIR, "cropped")
            resized_dir = os.path.join(OUTPUT_DIR, "resized")

            # ========== STEP 3: Run Processing Steps ==========
            if "Download" in steps:
                st.write("⬇️ Downloading photos...")
                os.makedirs(downloaded_dir, exist_ok=True)
                errors = download_photos(profiles, output_folder=downloaded_dir)
                if errors:
                    st.warning(f"{len(errors)} photos failed to download.")
                else:
                    st.success("All photos downloaded!")

            if "Crop" in steps:
                st.write("✂️ Cropping photos...")
                os.makedirs(cropped_dir, exist_ok=True)
                crop_photos_in_folder(downloaded_dir, cropped_dir)
                st.success("Cropping completed!")

            if "Resize" in steps:
                st.write("📏 Resizing photos...")
                os.makedirs(resized_dir, exist_ok=True)
                resize_photos_in_folder(cropped_dir, resized_dir)
                st.success("Resizing completed!")

            if "Validate" in steps:
                st.write("🔍 Validating photos...")
                results = validate_photos_in_folder(resized_dir)
                st.dataframe(pd.DataFrame(results))
                output_report = os.path.join(OUTPUT_DIR, "photo_validation_results.xlsx")
                save_validation_results(results, output_report, merge_original_df=df, left_on="Photo_Name", right_on="Photo_Name")
                st.success(f"Validation report saved: {output_report}")


            # ========== STEP 4: ZIP Download ==========
            zip_path = os.path.join(OUTPUT_DIR, "streamlit_output.zip")
            if os.path.exists(zip_path):
                os.remove(zip_path)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for foldername, subfolders, filenames in os.walk(OUTPUT_DIR):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, OUTPUT_DIR)
                        zipf.write(file_path, arcname=arcname)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All Results as ZIP",
                    data=f,
                    file_name="streamlit_output.zip",
                    mime="application/zip"
                )


# === 📁 Tab 2: Manual Image Upload ===
with tab2:
    st.subheader("Upload Images to Crop / Resize / Validate")

    uploaded_images = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_images:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save uploaded files to upload folder
        upload_folder = os.path.join(UPLOAD_DIR, "uploaded")
        os.makedirs(upload_folder, exist_ok=True)

        for file in uploaded_images:
            with open(os.path.join(upload_folder,file.name), "wb") as f:
                f.write(file.read())
        st.success(f"Uploaded {len(uploaded_images)} images.")

        # Let user choose which processing to apply
        process_steps = st.multiselect(
            "🔧 Choose operations to apply:",
            ["Crop", "Resize", "Validate"],
            default=["Crop", "Resize", "Validate"]
        )

        if st.button("🚀 Process Uploaded Images"):
            input_folder = upload_folder
            cropped_folder = os.path.join(UPLOAD_DIR, "cropped")
            resized_folder = os.path.join(UPLOAD_DIR, "resized")

            if "Crop" in process_steps:
                os.makedirs(cropped_folder, exist_ok=True)
                st.write("✂️ Cropping photos...")
                crop_photos_in_folder(input_folder, cropped_folder)
                st.success("Cropping completed!")
                input_folder = cropped_folder  # use cropped output for next step

            if "Resize" in process_steps:
                os.makedirs(resized_folder, exist_ok=True)
                st.write("📏 Resizing photos...")
                resize_photos_in_folder(input_folder, resized_folder)
                st.success("Resizing completed!")

            if "Validate" in process_steps:
                st.write("🔍 Validating photos...")
                validation_results = validate_photos_in_folder(resized_folder)
                st.dataframe(pd.DataFrame(validation_results))
                output_report = os.path.join(UPLOAD_DIR, "validation_results.xlsx")
                save_validation_results(validation_results, output_report)
                st.success(f"Validation report saved: {output_report}")

            st.info("🎉 Processing complete! You can now download your results.")

            zip_path = os.path.join(UPLOAD_DIR, "streamlit_output.zip")
            if os.path.exists(zip_path):
                os.remove(zip_path)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for foldername, subfolders, filenames in os.walk(UPLOAD_DIR):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, UPLOAD_DIR)
                        zipf.write(file_path, arcname=arcname)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download Processed Images as ZIP",
                    data=f,
                    file_name="streamlit_output.zip",
                    mime="application/zip"
                )