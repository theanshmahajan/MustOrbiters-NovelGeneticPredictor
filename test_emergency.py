#!/usr/bin/env python3
"""
Emergency Alert System Test Script
Test SMS and voice call functionality
"""

import sys
from datetime import datetime

def test_emergency_system():
    """Test the emergency alert system"""
    print("🧪 Testing Emergency Alert System")
    print("=" * 40)
    
    try:
        from emergency.config_manager import ConfigurationManager
        from emergency.alert_service import EmergencyAlertService, UrgencyLevel
        
        # Initialize services
        config_manager = ConfigurationManager()
        emergency_service = EmergencyAlertService(config_manager)
        
        # Check configuration
        twilio_config = config_manager.get_twilio_config()
        if not twilio_config or not twilio_config.is_configured:
            print("❌ Twilio not configured. Run setup_emergency.py first.")
            return False
        
        print("✅ Twilio configuration found")
        
        # Sample patient data
        sample_patient = {
            'age': 5,
            'gender': 1,  # Male
            'case_id': f"TEST_{datetime.now().strftime('%H%M%S')}",
            'seizures': 1,
            'developmental_delay': 1,
            'cardiac_abnormalities': 0
        }
        
        print("\n📋 Sample Patient Data:")
        print(f"   Age: {sample_patient['age']} years")
        print(f"   Gender: {'Male' if sample_patient['gender'] == 1 else 'Female'}")
        print(f"   Case ID: {sample_patient['case_id']}")
        print(f"   Symptoms: Seizures, Developmental Delay")
        
        # Test emergency alert
        print(f"\n🚨 Sending test emergency alert to +91-831-961-2060...")
        
        success, message, alert = emergency_service.send_emergency_alert(
            patient_data=sample_patient,
            urgency_level=UrgencyLevel.HIGH,
            user_notes="Test emergency alert from NGP system",
            phone_number="+918319612060"
        )
        
        if success:
            print(f"✅ {message}")
            if alert:
                print(f"\n📊 Alert Details:")
                print(f"   Alert ID: {alert.alert_id}")
                print(f"   Timestamp: {alert.timestamp}")
                print(f"   Urgency: {alert.urgency_level.value}")
                print(f"   SMS Content: {alert.message_content}")
                if alert.message_sid:
                    print(f"   SMS SID: {alert.message_sid}")
                if alert.call_sid:
                    print(f"   Call SID: {alert.call_sid}")
        else:
            print(f"❌ {message}")
            return False
        
        print("\n🎉 Emergency alert test completed!")
        print("📱 Check your phone for SMS and voice call")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure emergency system is set up properly")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧬 NGP Emergency Alert System Test")
    print()
    
    # Run test
    success = test_emergency_system()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("🚀 Emergency system is ready for use in the main application")
    else:
        print("\n❌ Test failed. Please check configuration and try again.")
        print("💡 Run setup_emergency.py to configure the system")

if __name__ == "__main__":
    main()