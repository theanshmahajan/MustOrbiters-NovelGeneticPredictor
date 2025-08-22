#!/usr/bin/env python3
"""
Simple configuration script for Indian phone number +918319612060
"""

from emergency.config_manager import ConfigurationManager
from emergency.alert_service import EmergencyAlertService, UrgencyLevel

def configure_for_india():
    print("🇮🇳 Configuring Emergency System for India")
    print("Phone Number: +91-831-961-2060")
    print("=" * 50)
    
    # Get Twilio credentials from user
    print("\n📱 Enter your Twilio credentials:")
    print("(Get these from: https://console.twilio.com/)")
    
    account_sid = input("Account SID (starts with AC...): ").strip()
    if not account_sid:
        print("❌ Account SID is required")
        return False
    
    auth_token = input("Auth Token: ").strip()
    if not auth_token:
        print("❌ Auth Token is required")
        return False
    
    from_number = input("Your Twilio Phone Number (e.g., +1234567890): ").strip()
    if not from_number:
        print("❌ Twilio phone number is required")
        return False
    
    # Configure the system
    print("\n💾 Saving configuration...")
    config_manager = ConfigurationManager()
    
    # Save Twilio config
    success = config_manager.save_twilio_config(
        account_sid=account_sid,
        auth_token=auth_token,
        from_number=from_number
    )
    
    if not success:
        print("❌ Failed to save Twilio configuration")
        return False
    
    print("✅ Twilio configuration saved!")
    
    # Add Indian phone number as emergency contact
    contact_success = config_manager.add_emergency_contact(
        name="Indian Phone Number",
        phone_number="+918319612060",
        priority=1
    )
    
    if contact_success:
        print("✅ Indian phone number +918319612060 added as emergency contact")
    else:
        print("⚠️ Warning: Could not add emergency contact")
    
    # Test the configuration
    print("\n🧪 Testing SMS to +918319612060...")
    emergency_service = EmergencyAlertService(config_manager)
    
    test_sms = input("Send test SMS now? (y/n): ").strip().lower()
    if test_sms == 'y':
        success, message = emergency_service.test_sms_configuration("+918319612060")
        print(f"\n📱 SMS Test Result: {message}")
        
        if success:
            print("✅ Check your phone +918319612060 for test SMS!")
        else:
            print("❌ SMS test failed. Check your Twilio configuration.")
            print("💡 Make sure +918319612060 is verified in your Twilio account")
    
    # Test emergency alert
    test_emergency = input("\nSend test emergency alert (SMS + Voice)? (y/n): ").strip().lower()
    if test_emergency == 'y':
        print("🚨 Sending test emergency alert...")
        
        sample_patient = {
            'age': 25,
            'gender': 1,  # Male
            'case_id': 'TEST_INDIA_001',
            'seizures': 1,
            'developmental_delay': 0
        }
        
        success, message, alert = emergency_service.send_emergency_alert(
            patient_data=sample_patient,
            urgency_level=UrgencyLevel.HIGH,
            user_notes="Test emergency alert for Indian phone number",
            phone_number="+918319612060"
        )
        
        print(f"\n🚨 Emergency Alert Result: {message}")
        
        if success:
            print("✅ Emergency alert sent!")
            print("📱 Check your phone +918319612060 for:")
            print("   • SMS with patient details")
            print("   • Voice call with emergency message")
            
            if alert:
                print(f"\n📊 Alert Details:")
                print(f"   Alert ID: {alert.alert_id}")
                print(f"   Urgency: {alert.urgency_level.value}")
                print(f"   SMS Content: {alert.message_content}")
        else:
            print("❌ Emergency alert failed")
            print("💡 Common issues:")
            print("   • Phone number not verified in Twilio")
            print("   • Insufficient Twilio account balance")
            print("   • International calling restrictions")
    
    print("\n🎉 Configuration Complete!")
    print("=" * 50)
    print("✅ Emergency system configured for +918319612060")
    print("✅ Ready to use in NGP application")
    print("\n🚀 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Go to Patient Diagnosis tab")
    print("3. Enter patient data")
    print("4. Click 🚨 EMERGENCY ALERT button")
    print("5. You'll receive SMS and voice call!")
    
    return True

if __name__ == "__main__":
    try:
        configure_for_india()
    except KeyboardInterrupt:
        print("\n\n👋 Configuration cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you have installed: pip install twilio cryptography")