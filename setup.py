#!/usr/bin/env python3
"""
Setup script for YouTube AI Content Analysis
"""
import os
import sys
import subprocess
import shutil


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("📝 Please edit .env and add your YouTube API key")
        else:
            # Create a basic .env file
            with open('.env', 'w') as f:
                f.write("# YouTube Data API v3 Key\n")
                f.write("# Get it from: https://console.cloud.google.com/apis/credentials\n")
                f.write("YOUTUBE_API_KEY=your_youtube_api_key_here\n\n")
                f.write("# OpenAI API Key (optional, for advanced content generation)\n")
                f.write("# Get it from: https://platform.openai.com/api-keys\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            print("✅ Created .env file")
            print("📝 Please edit .env and add your YouTube API key")
    else:
        print("✅ .env file already exists")
    
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['output', 'demo_output']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/ directory")
        else:
            print(f"✅ {directory}/ directory already exists")
    
    return True


def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        'pandas',
        'requests',
        'google.auth',
        'googleapiclient.discovery',
        'dotenv'
    ]
    
    failed_imports = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All required modules imported successfully")
    return True


def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    
    print("\n📝 Next Steps:")
    print("1. Get your YouTube API key:")
    print("   • Go to https://console.cloud.google.com/apis/credentials")
    print("   • Create a new project or select existing one")
    print("   • Enable YouTube Data API v3")
    print("   • Create credentials (API Key)")
    print("   • Add the key to your .env file")
    
    print("\n2. Test the system:")
    print("   • Run demo: python demo.py")
    print("   • Run full analysis: python main.py")
    
    print("\n3. Customize configuration:")
    print("   • Edit config.py to adjust thresholds")
    print("   • Add AI keywords and influencers")
    print("   • Modify content templates")
    
    print("\n📚 Documentation:")
    print("   • Read README_YOUTUBE_AI_ANALYSIS.md for detailed instructions")
    print("   • Check output/ directory for generated CSV files")
    
    print("\n🚀 Ready to analyze AI content and generate viral ideas!")


def main():
    """Main setup function"""
    print("🚀 YouTube AI Content Analysis - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n💡 Try installing dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n💡 Try reinstalling dependencies:")
        print("   pip install --upgrade -r requirements.txt")
        sys.exit(1)
    
    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    main()