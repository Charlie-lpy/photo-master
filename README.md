# 🖼️ photo-master

A lightweight and user-friendly Python app for **batch downloading**, **cropping**, and **resizing** profile photos using an Excel report as input. Built with ❤️ using Python and Streamlit — no coding skills required!

## 🚀 Features

- 🔽 **Batch download** photos from image URLs in Excel
- ✂️ **Crop** images automatically to the desired aspect ratio (e.g., 3:4)
- 📏 **Resize** photos to meet file size limits (e.g., 50KB–1MB)
- ✅ **Validate** image dimensions and generate reports

## 📦 Installation and Environment Set-up

### 1. Install Python  
Download and install Python from [python.org](https://www.python.org/downloads).  
Make sure to check ✅ **"Add Python to PATH"** during installation.

### 2. Download This Repository

- Go to the repo in your browser:  
   👉 [https://github.com/Charlie-lpy/photo-master](https://github.com/Charlie-lpy/photo-master)

- Click the green **"Code"** button, then select **"Download ZIP"**

- After downloading, **extract the ZIP file** to a folder on your computer (e.g., `D:\photo-master`)

### 3. Open a terminal (Command Prompt)

- **Windows**:  
Press `Win + R`, type `cmd`, and hit Enter to open the Command Prompt.

- **macOS**:  
Press `Cmd + Space`, type `Terminal`, and hit Enter.

- **Linux**:  
  Use `Ctrl + Alt + T`, or search for “Terminal” in your applications menu.
  
### 4. Navigate to the Project Folder

Use the `cd` command to move into the folder where you downloaded or cloned this project:

```bash
cd path/to/your/photo-master
```

Replace  `path/to/your/...` with the actual folder path.

Once you're in the project folder, you're ready to **create a virtual environment and install dependencies**!

### 5. Create and Activate a Virtual Environment

```bash
python -m venv venv
```
Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 6. Install Required Packages

```bash
pip install -r requirements.txt
```

## 🌐 Usage with Streamlit Web App

Follow these steps to launch the App on your local machine:

### 1. Open a Terminal (Command Prompt)

- **Windows**:  
Press `Win + R`, type `cmd`, and hit Enter to open the Command Prompt.

- **macOS**:  
Press `Cmd + Space`, type `Terminal`, and hit Enter.

- **Linux**:  
  Use `Ctrl + Alt + T`, or search for “Terminal” in your applications menu.

### 2. Navigate to the Project Folder

Use the `cd` command to move into the folder where you downloaded or cloned this project:

```bash
cd path/to/your/photo-master
```

Replace  `path/to/your/...` with the actual folder path.

### 3. Activate your Python Virtual Environment

If you followed the setup steps and created a `venv` virtual environment in the project folder, activate it:

```bash
# For windows:
venv\Scripts\activate

# For macOS/Linux:
source venv/bin/activate
```

### 4. Run the App with Streamlit:

```bash
streamlit run app.py
```

A web interface will open in your browser.  
Upload your Excel file and process photos in just a few clicks!

### 🗒️ Excel Input Requirements

Your Excel file should include columns like:

- **`Confirmation_Number`**: Unique identifier for each person
- **`Image_URL`**: Direct link to each photo
- **`Photo_Name`**: Desired filename

## 💻 Usage from the Terminal (Advanced)

### Run the full pipeline:

```bash
python main.py
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

For a full list of arguments, run:
```bash
python main.py --help
```

## 👩🏻‍💻 Author

Developed by **Charlotte LYU**  
For questions, suggestions, or collaboration, please reach out!
