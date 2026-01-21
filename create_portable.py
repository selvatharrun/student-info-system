"""
Setup script to create a portable Student Info System.
This downloads embedded Python and installs all dependencies - no admin rights needed.
Run this ONCE on your PC, then copy the entire folder to USB/college PC.
"""
import urllib.request
import zipfile
import os
import subprocess
import shutil

PYTHON_VERSION = "3.11.9"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"

def main():
    print("=" * 60)
    print("  PORTABLE STUDENT INFO SYSTEM - SETUP")
    print("=" * 60)
    
    # Create portable folder
    portable_dir = "portable"
    python_dir = os.path.join(portable_dir, "python")
    
    if os.path.exists(portable_dir):
        print(f"\n[!] Removing existing '{portable_dir}' folder...")
        shutil.rmtree(portable_dir)
    
    os.makedirs(python_dir, exist_ok=True)
    
    # Download Python Embedded
    print(f"\n[1/5] Downloading Python {PYTHON_VERSION} Embedded...")
    zip_path = os.path.join(portable_dir, "python.zip")
    urllib.request.urlretrieve(PYTHON_URL, zip_path)
    
    # Extract Python
    print("[2/5] Extracting Python...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
    os.remove(zip_path)
    
    # Enable pip by modifying python311._pth file
    print("[3/5] Configuring Python for pip...")
    pth_file = os.path.join(python_dir, f"python311._pth")
    with open(pth_file, 'w') as f:
        f.write("python311.zip\n")
        f.write(".\n")
        f.write("Lib\\site-packages\n")
        f.write("import site\n")
    
    # Download and install pip
    print("[4/5] Installing pip...")
    get_pip_path = os.path.join(portable_dir, "get-pip.py")
    urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
    
    python_exe = os.path.join(python_dir, "python.exe")
    subprocess.run([python_exe, get_pip_path, "--no-warn-script-location"], check=True)
    os.remove(get_pip_path)
    
    # Install dependencies
    print("[5/5] Installing app dependencies (this may take a few minutes)...")
    subprocess.run([
        python_exe, "-m", "pip", "install",
        "streamlit", "pandas", "pandasai", "openai", "openpyxl", "pyyaml",
        "--no-warn-script-location", "-q"
    ], check=True)
    
    # Copy app files
    print("\n[+] Copying app files...")
    shutil.copy("app.py", portable_dir)
    shutil.copy("config.yaml", portable_dir)
    shutil.copy("requirements.txt", portable_dir)
    
    # Create run script
    run_bat = os.path.join(portable_dir, "START_APP.bat")
    with open(run_bat, 'w') as f:
        f.write('@echo off\n')
        f.write('echo ========================================\n')
        f.write('echo   Student Info System\n')
        f.write('echo ========================================\n')
        f.write('echo.\n')
        f.write('echo Starting app... Please wait.\n')
        f.write('echo The browser will open automatically.\n')
        f.write('echo Close this window to stop the server.\n')
        f.write('echo.\n')
        f.write('cd /d "%~dp0"\n')
        f.write('python\\python.exe -m streamlit run app.py --server.headless true\n')
        f.write('pause\n')
    
    print("\n" + "=" * 60)
    print("  SETUP COMPLETE!")
    print("=" * 60)
    print(f"""
Your portable app is ready in the 'portable' folder!

TO USE ON COLLEGE PC:
  1. Copy the entire 'portable' folder to a USB drive
  2. On the college PC, open the 'portable' folder
  3. Double-click 'START_APP.bat'
  4. Browser opens at http://localhost:8501

Folder size: ~500MB (includes Python + all libraries)
No installation or admin rights required!
""")

if __name__ == "__main__":
    main()
