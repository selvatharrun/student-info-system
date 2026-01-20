"""
Launcher script for Student Info System
This starts the Streamlit server and opens the browser automatically.
"""
import subprocess
import sys
import os
import time
import webbrowser
import socket

def find_free_port():
    """Find a free port to run the server on."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def main():
    # Get the directory where this script/exe is located
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    app_path = os.path.join(app_dir, 'app.py')
    port = 8501
    
    print("🎓 Starting Student Info System...")
    print(f"   App directory: {app_dir}")
    print(f"   Port: {port}")
    
    # Start Streamlit server
    process = subprocess.Popen(
        [
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--server.address', 'localhost'
        ],
        cwd=app_dir
    )
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Open browser
    url = f'http://localhost:{port}'
    print(f"   Opening browser: {url}")
    webbrowser.open(url)
    
    print("\n✅ App is running! Close this window to stop the server.")
    print("   Press Ctrl+C to stop.\n")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        process.terminate()

if __name__ == '__main__':
    main()
