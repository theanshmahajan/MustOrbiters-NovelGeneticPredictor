#!/usr/bin/env python3
"""
Emergency Alert System Setup Script
Quick setup for Twilio SMS and Voice Call functionality
"""

import os
import sys

def setup_emergency_system():
    """Setup emergency alert system with Twilio"""
    print("🚨 Emergency Alert System Setup")
    print("=" * 50)
    
    # Check if emergency module exists
    if not os.path.exists('emergency'):
        print("❌ Emergency module not found. Please ensure all files are in place.")
        return False
    
    try:
        from emergency.config_manager import ConfigurationManager
        from emergency.alert_service import EmergencyAlertService
        
        print("✅ Emergency modules loaded successfully")
        
        # Initialize configuration manager
        config_manager = ConfigurationManager()
        
        print("\n📱 Twilio Configuration Required")
        print("You need a Twilio account to send SMS and make voice calls.")
        print("Sign up at: https://www.twilio.com/try-twilio")
        print()
        
        # Get Twilio credentials
        account_sid = input("Enter your Twilio Account SID: ").strip()
        if not account_sid:
            print("❌ Account SID is required")
            return False
        
        auth_token = input("Enter your Twilio Auth Token: ").strip()
        if not auth_token:
            print("❌ Auth Token is required")
            return False
        
        from_number = input("Enter your Twilio Phone Number (e.g., +1234567890): ").strip()
        if not from_number:
            print("❌ From phone number is required")
            return False
        
        # Save configuration
        print("\n💾 Saving configuration...")
        success = config_manager.save_twilio_config(
            account_sid=account_sid,
            auth_token=auth_token,
            from_number=from_number
        )
        
        if not success:
            print("❌ Failed to save configuration")
            return False
        
        print("✅ Configuration saved successfully!")
        
        # Add emergency contact (your phone number)
        print("\n📞 Adding emergency contact...")
        contact_success = config_manager.add_emergency_contact(
            name="Primary Emergency Contact",
            phone_number="+918319612060",
            priority=1
        )
        
        if contact_success:
            print("✅ Emergency contact added: +91-831-961-2060 (India)")
        else:
            print("⚠️ Warning: Could not add emergency contact")
        
        # Test the configuration
        print("\n🧪 Testing SMS configuration...")
        emergency_service = EmergencyAlertService(config_manager)
        
        test_choice = input("Send test SMS to +91-831-961-2060? (y/n): ").strip().lower()
        if test_choice == 'y':
            success, message = emergency_service.test_sms_configuration("+918319612060")
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
        
        print("\n🎉 Emergency Alert System Setup Complete!")
        print("=" * 50)
        print("✅ Twilio configured")
        print("✅ Emergency contact added")
        print("✅ Ready to send SMS and voice alerts")
        print()
        print("🚀 Run your NGP application with: streamlit run app.py")
        print("🚨 Emergency button will be available in the Patient Diagnosis tab")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install twilio cryptography")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def main():
    """Main setup function"""
    print("🧬 Novel Genetic Predictor - Emergency Alert Setup")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return
    
    # Install required packages
    print("📦 Checking required packages...")
    try:
        import twilio
        import cryptography
        print("✅ Required packages available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Install with: pip install twilio cryptography")
        return
    
    # Run setup
    success = setup_emergency_system()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Run: streamlit run app.py")
        print("2. Go to Patient Diagnosis tab")
        print("3. Enter patient data")
        print("4. Click the red 🚨 EMERGENCY ALERT button")
        print("5. You'll receive SMS and voice call at +91-831-961-2060")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()