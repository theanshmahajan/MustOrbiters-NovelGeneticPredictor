#!/usr/bin/env python3
"""
Quick test to verify emergency system works with your Twilio credentials
"""

from emergency.config_manager import ConfigurationManager
from emergency.alert_service import EmergencyAlertService, UrgencyLevel
from datetime import datetime

def quick_test():
    print("🚨 Quick Emergency System Test")
    print("Using your Twilio credentials:")
    print("Account SID: AC0dddc74f9a425bb1003e302daac8b94f")
    print("From Number: +15513683290")
    print("Target: +91-831-961-2060")
    print("=" * 50)
    
    try:
        # Initialize services
        config_manager = ConfigurationManager()
        emergency_service = EmergencyAlertService(config_manager)
        
        # Check configuration
        twilio_config = config_manager.get_twilio_config()
        if not twilio_config or not twilio_config.is_configured:
            print("❌ Twilio not configured")
            return False
        
        print("✅ Twilio configuration loaded")
        
        # Sample patient data (like from main app)
        patient_data = {
            'age': 8,
            'gender': 1,  # Male
            'case_id': f"MAIN_APP_TEST_{datetime.now().strftime('%H%M%S')}",
            'seizures': 1,
            'cardiac_abnormalities': 1,
            'developmental_delay': 0,
            'height_cm': 130,
            'weight_kg': 30,
            'bp_systolic': 110,
            'bp_diastolic': 75
        }
        
        print("\n📋 Sample Patient Data (like from main app):")
        print(f"   Age: {patient_data['age']} years")
        print(f"   Gender: Male")
        print(f"   Case ID: {patient_data['case_id']}")
        print(f"   Symptoms: Seizures, Cardiac Issues")
        
        # Send emergency alert (exactly like main app would)
        print(f"\n🚨 Sending emergency alert to +91-831-961-2060...")
        
        success, message, alert = emergency_service.send_emergency_alert(
            patient_data=patient_data,
            urgency_level=UrgencyLevel.HIGH,
            user_notes="Test from main app simulation",
            phone_number="+918319612060"
        )
        
        if success:
            print(f"✅ {message}")
            print("\n📱 You should receive:")
            print("   • SMS with patient details")
            print("   • Voice call with emergency message")
            
            if alert:
                print(f"\n📊 Alert Details:")
                print(f"   Alert ID: {alert.alert_id}")
                print(f"   Urgency: {alert.urgency_level.value}")
                print(f"   SMS Content: {alert.message_content}")
                print(f"   SMS SID: {alert.message_sid}")
                print(f"   Call SID: {alert.call_sid}")
            
            print("\n🎉 Emergency system working perfectly!")
            print("This is exactly what happens when you click the emergency button in the main app.")
            return True
        else:
            print(f"❌ {message}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if quick_test():
        print("\n✅ Emergency system is working!")
        print("🚀 The main app emergency button should work the same way.")
        print("\nTo run main app:")
        print("1. python -m streamlit run app.py")
        print("2. Go to Patient Diagnosis tab")
        print("3. Enter patient data")
        print("4. Click 🚨 EMERGENCY ALERT button")
        print("5. You'll get SMS + voice call!")
    else:
        print("\n❌ Emergency system has issues.")
        print("💡 Check your Twilio configuration.")