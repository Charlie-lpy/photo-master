# 🖼️ photo-master
A lightweight and user-friendly Python app for **batch downloading**, **cropping**, and **resizing** profile photos using an Excel report as input.  
Built with ❤️ using Python and Streamlit — no coding skills required!

## 🚀 Features

- 🔽 **Batch download** photos from image URLs in Excel
- ✂️ **Crop** images automatically to the desired aspect ratio (e.g., 3:4)
- 📏 **Resize** photos to meet file size limits (e.g., 50KB–1MB)
- ✅ **Validate** image dimensions and generate reports

## 📦 Installation

### 1. Install Python  
Download and install Python from [python.org](https://www.python.org/downloads).  
Make sure to check ✅ **"Add Python to PATH"** during installation.

### 📥 2. Clone or Download This Repository (For Beginners)

If you're new to Git or just want the easiest way:

- Go to the repo in your browser:  
   👉 [https://github.com/Charlie-lpy/photo-master](https://github.com/Charlie-lpy/photo-master)

- Click the green **"Code"** button, then select **"Download ZIP"**

- After downloading, **extract the ZIP file** to a folder on your computer (e.g., `D:\photo-master`)

- Open a terminal (Command Prompt), and navigate to that folder:
   ```bash
   cd path\to\your\photo-master
   ```

Once you're in the project folder, you're ready to set up the environment!
   

### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

## 🏃‍♀️ Usage on Website (Streamlit)

Just run the app using Streamlit:
```bash
streamlit run main.py
```
A web interface will open in your browser.
Upload your Excel file and start processing photos with just a few clicks!

### 🗒️ Excel Input Requirements

Your Excel file should include columns like:

- **`Confirmation_Number`**: Unique identifier for each person
- **`Image_URL`**: Direct link to each photo
- **`Photo_Name`**: Desired filename (optional, can use Confirmation Number)


## 🏃‍♀️ Usage in Terminal (Python)

### Run the full pipeline:
```bash
python main.py --tool all
```

### Or run individual steps:
```bash
python main.py --tool download
python main.py --tool validate
python main.py --tool crop
python main.py --tool resize
```

### Customize input/output paths (example)
```bash
python main.py --tool download \
    --download_input_report data/raw_reports/my_input.xlsx \
    --download_photo_folder photos/my_downloads
```
All arguments are listed in main.py or with python main.py --help


## 👩🏻‍💻 Author

Developed by **Charlotte LYU**  
For questions, suggestions, or collaboration, please reach out!
