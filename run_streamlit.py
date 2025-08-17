#!/usr/bin/env python3
"""
Quick start script for Data Analyst Agent Streamlit application
Run this script to launch the web application
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main function to start the Streamlit application"""
    
    print("🚀 Starting Data Analyst Agent...")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    src_dir = current_dir / "src"
    
    if not src_dir.exists():
        print("❌ Error: 'src' directory not found.")
        print("Make sure you're running this script from the project root directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import streamlit
        import pandas
        import together
        print("✅ Required packages found")
    except ImportError as e:
        print(f"❌ Missing required package: {e.name}")
        print("\nPlease install requirements first:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check for .env file
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
        print("Please copy .env.example to .env and add your API key:")
        print("cp .env.example .env")
        print("\nYou can still run the app and enter your API key in the sidebar.")
        print()
    
    # Launch Streamlit
    streamlit_script = src_dir / "streamlit_app.py"
    
    try:
        print(f"🌐 Launching Streamlit application...")
        print(f"📁 Script: {streamlit_script}")
        print("🔗 The app will open in your default browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(streamlit_script),
            "--server.address", "localhost",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
