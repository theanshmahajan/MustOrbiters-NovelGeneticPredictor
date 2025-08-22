#!/usr/bin/env python3
"""
Test the main app emergency system without running Streamlit
"""

def test_main_app_imports():
    print("🧪 Testing Main App Emergency Imports")
    print("=" * 50)
    
    try:
        # Test emergency system imports (same as app.py)
        from emergency.config_manager import ConfigurationManager
        from emergency.alert_service import EmergencyAlertService, UrgencyLevel
        from emergency.ui_components import render_emergency_button, render_emergency_dialog, render_emergency_settings
        print("✅ Emergency system imports successful")
        
        # Test initialization (same as app.py)
        config_manager = ConfigurationManager()
        emergency_service = EmergencyAlertService(config_manager)
        print("✅ Emergency service initialized")
        
        # Test configuration check (same as app.py)
        twilio_config = config_manager.get_twilio_config()
        if twilio_config and twilio_config.is_configured:
            print("✅ Twilio configuration found")
            print(f"   From: {twilio_config.from_phone_number}")
            print(f"   Target: +91-831-961-2060")
            emergency_configured = True
        else:
            print("❌ Twilio not configured")
            emergency_configured = False
        
        # Test emergency alert (same as what main app would do)
        if emergency_configured:
            print("\n🚨 Testing emergency alert (same as main app)...")
            
            patient_data = {
                'age': 10,
                'gender': 1,
                'case_id': 'MAIN_APP_SIM_001',
                'seizures': 1,
                'cardiac_abnormalities': 1
            }
            
            success, message, alert = emergency_service.send_emergency_alert(
                patient_data=patient_data,
                urgency_level=UrgencyLevel.HIGH,
                user_notes="Test from main app simulation",
                phone_number="+918319612060"
            )
            
            if success:
                print(f"✅ {message}")
                print("📱 Check your phone +91-831-961-2060!")
                return True
            else:
                print(f"❌ {message}")
                return False
        else:
            print("❌ Cannot test - Twilio not configured")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧬 NGP Main App Emergency System Test")
    print("Testing the exact same code that runs in app.py")
    print()
    
    if test_main_app_imports():
        print("\n🎉 Main app emergency system should work!")
        print("The issue might be in the Streamlit UI, not the core functionality.")
        print("\n🚀 Try running: python -m streamlit run app.py")
        print("Look for the 'DIRECT EMERGENCY ALERT' button in Patient Diagnosis tab")
    else:
        print("\n❌ Main app emergency system has issues")
        print("💡 Run: python configure_india.py")