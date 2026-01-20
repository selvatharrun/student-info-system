"""
Build script to create a standalone executable.
Run this with: python build_exe.py
"""
import subprocess
import sys
import os

def main():
    print("📦 Building Student Info System executable...")
    print("=" * 50)
    
    # Install PyInstaller if not present
    print("\n1. Checking PyInstaller...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Build the executable
    print("\n2. Building executable...")
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--name=StudentInfoSystem',
        '--onedir',  # Creates a folder with all dependencies
        '--console',  # Show console window (useful for seeing server logs)
        '--add-data=app.py;.',
        '--add-data=config.yaml;.',
        '--hidden-import=streamlit',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=yaml',
        '--hidden-import=pydantic',
        '--collect-all=streamlit',
        '--collect-all=altair',
        '--copy-metadata=streamlit',
        '--noconfirm',  # Overwrite without asking
        'launcher.py'
    ], check=True)
    
    print("\n" + "=" * 50)
    print("✅ Build complete!")
    print("\nYour app is in the 'dist/StudentInfoSystem' folder.")
    print("To share: Copy the entire 'StudentInfoSystem' folder to another PC.")
    print("To run: Double-click 'StudentInfoSystem.exe'")

if __name__ == '__main__':
    main()
