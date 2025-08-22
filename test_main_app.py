#!/usr/bin/env python3
"""
Test script to check if main app.py loads emergency system correctly
"""

import sys
import os

def test_main_app_emergency():
    print("🧪 Testing Main App Emergency System Integration")
    print("=" * 60)
    
    # Test imports
    print("1. Testing imports...")
    try:
        from emergency.config_manager import ConfigurationManager
        from emergency.alert_service import EmergencyAlertService
        from emergency.ui_components import render_emergency_button, render_emergency_dialog, render_emergency_settings
        print("   ✅ Emergency system imports successful")
    except ImportError as e:
        print(f"   ❌ Emergency system import failed: {e}")
        return False
    
    # Test configuration
    print("\n2. Testing configuration...")
    try:
        config_manager = ConfigurationManager()
        twilio_config = config_manager.get_twilio_config()
        
        if twilio_config and twilio_config.is_configured:
            print("   ✅ Twilio configuration found")
            print(f"   📱 From Number: {twilio_config.from_phone_number}")
            print(f"   🎯 Target: +91-831-961-2060")
        else:
            print("   ❌ Twilio not configured")
            print("   💡 Run: python configure_india.py")
            return False
            
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False
    
    # Test emergency service initialization
    print("\n3. Testing emergency service...")
    try:
        emergency_service = EmergencyAlertService(config_manager)
        print("   ✅ Emergency service initialized")
    except Exception as e:
        print(f"   ❌ Emergency service failed: {e}")
        return False
    
    # Test quick SMS
    print("\n4. Testing SMS functionality...")
    try:
        success, message = emergency_service.test_sms_configuration("+918319612060")
        if success:
            print(f"   ✅ {message}")
            print("   📱 Check your phone +91-831-961-2060 for test SMS!")
        else:
            print(f"   ❌ {message}")
            return False
    except Exception as e:
        print(f"   ❌ SMS test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Main app should work correctly.")
    print("=" * 60)
    print("🚀 Run: python -m streamlit run app.py")
    print("📱 Emergency button should appear in Patient Diagnosis tab")
    
    return True

def check_streamlit_availability():
    print("🔍 Checking Streamlit availability...")
    try:
        import streamlit
        print(f"   ✅ Streamlit version: {streamlit.__version__}")
        return True
    except ImportError:
        print("   ❌ Streamlit not installed")
        print("   💡 Run: pip install streamlit")
        return False

if __name__ == "__main__":
    print("🧬 NGP Main App Emergency System Test")
    print()
    
    # Check Streamlit
    if not check_streamlit_availability():
        sys.exit(1)
    
    # Test emergency system
    if test_main_app_emergency():
        print("\n✅ Ready to run main application!")
        
        # Ask if user wants to run the app
        run_app = input("\nRun main app now? (y/n): ").strip().lower()
        if run_app == 'y':
            print("🚀 Starting main NGP application...")
            os.system("python -m streamlit run app.py")
    else:
        print("\n❌ Tests failed. Please fix issues before running main app.")
        print("💡 Try running: python configure_india.py")