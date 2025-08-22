#!/usr/bin/env python3
"""
Enhanced setup script for the Novel Genetic Predictor project
Compatible with Python 3.13 and handles common installation issues
"""

import os
import subprocess
import sys
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8 or higher is required")
        return False

def install_requirements():
    """Install required packages with Python 3.13 compatibility"""
    print("📦 Installing required packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install packages one by one to handle potential conflicts
        packages = [
            "streamlit>=1.28.0",
            "pandas>=2.1.0", 
            "numpy>=1.24.0",
            "tensorflow>=2.15.0",
            "plotly>=5.17.0",
            "scikit-learn>=1.3.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Warning: Failed to install {package}: {e}")
                
                # Try alternative installation methods for problematic packages
                if "tensorflow" in package:
                    print("🔧 Trying alternative TensorFlow installation...")
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "tensorflow-cpu>=2.15.0"])
                    except:
                        print("⚠️  TensorFlow installation failed. The app will work with limited functionality.")
                
        print("✅ Package installation completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install requirements: {e}")
        print("💡 Try running: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["models", "data", "logs"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created/verified directory: {directory}")

def verify_installation():
    """Verify that key packages can be imported"""
    print("🔍 Verifying installation...")
    
    required_imports = {
        'streamlit': 'streamlit',
        'pandas': 'pandas', 
        'numpy': 'numpy',
        'plotly': 'plotly.express',
    }
    
    optional_imports = {
        'tensorflow': 'tensorflow',
        'sklearn': 'sklearn',
        'matplotlib': 'matplotlib.pyplot',
        'seaborn': 'seaborn'
    }
    
    all_good = True
    
    # Check required imports
    for name, module in required_imports.items():
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {name}: {e}")
            all_good = False
    
    # Check optional imports
    for name, module in optional_imports.items():
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"⚠️  Optional package {name} not available: {e}")
    
    return all_good

def run_app():
    """Run the Streamlit application"""
    print("🚀 Starting the Novel Genetic Predictor application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        # Change to the directory containing app.py
        if os.path.exists('app.py'):
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        else:
            print("❌ app.py not found in current directory")
            print("📁 Make sure you're in the project root directory")
            
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Thank you for using NGP!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("🔄 Please run this script again")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup function"""
    print("🧬 Novel Genetic Predictor (NGP) Setup")
    print("=" * 50)
    print(f"💻 Operating System: {platform.system()} {platform.release()}")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Some packages failed to install, but continuing...")
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Some required packages are missing, but attempting to continue...")
    
    print("\n🎯 Setup complete! Starting the application...")
    print("=" * 50)
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main()