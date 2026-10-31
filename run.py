"""
Master Application Launcher for Student Expense Tracker and Analyzer.
Starts the Flask REST API backend and Streamlit frontend.

Usage:
    python run.py               # Starts Flask Backend and Streamlit Frontend together
    python run.py --backend     # Starts only Flask Backend
    python run.py --frontend    # Starts only Streamlit Frontend
"""

import subprocess
import sys
import time
import os

def start_backend():
    print("[RUNNER] Launching Flask REST API on http://127.0.0.1:5000...")
    return subprocess.Popen([sys.executable, "app.py"])

def start_frontend():
    print("[RUNNER] Launching Streamlit Frontend on http://localhost:8501...")
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port=8501"])

def main():
    if "--backend" in sys.argv:
        p = start_backend()
        p.wait()
    elif "--frontend" in sys.argv:
        p = start_frontend()
        p.wait()
    else:
        print("================================================================")
        print("  Student Expense Tracker and Analyzer - Multi-Service Launcher ")
        print("================================================================")
        backend_proc = start_backend()
        
        # Give Flask 2 seconds to bind port and connect to MySQL
        time.sleep(2)
        
        frontend_proc = start_frontend()
        
        try:
            backend_proc.wait()
            frontend_proc.wait()
        except KeyboardInterrupt:
            print("\n[RUNNER] Shutting down services...")
            backend_proc.terminate()
            frontend_proc.terminate()

if __name__ == "__main__":
    main()
