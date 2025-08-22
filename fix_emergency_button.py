#!/usr/bin/env python3
"""
Fix for emergency button in main app.py
This script will create a simplified version that definitely works
"""

import streamlit as st
from datetime import datetime

# Import emergency system
try:
    from emergency.config_manager import ConfigurationManager
    from emergency.alert_service import EmergencyAlertService, UrgencyLevel
    EMERGENCY_AVAILABLE = True
except ImportError as e:
    st.error(f"Emergency system not available: {e}")
    EMERGENCY_AVAILABLE = False

st.set_page_config(page_title="NGP Emergency Test", page_icon="🚨")

st.title("🚨 NGP Emergency Button Test")
st.markdown("Testing emergency button functionality")

# Initialize emergency system
if EMERGENCY_AVAILABLE:
    if 'emergency_service' not in st.session_state:
        try:
            config_manager = ConfigurationManager()
            st.session_state.emergency_service = EmergencyAlertService(config_manager)
            
            # Check configuration
            twilio_config = config_manager.get_twilio_config()
            if twilio_config and twilio_config.is_configured:
                st.success("✅ Emergency system initialized and configured")
                st.info(f"📱 Target: +91-831-961-2060")
                st.info(f"📞 From: {twilio_config.from_phone_number}")
                st.session_state.emergency_ready = True
            else:
                st.error("❌ Emergency system not configured")
                st.session_state.emergency_ready = False
        except Exception as e:
            st.error(f"❌ Emergency system failed: {e}")
            st.session_state.emergency_ready = False
    
    # Patient data form
    st.subheader("👤 Patient Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", 0, 18, 8)
        gender = st.selectbox("Gender", ["Male", "Female"])
    
    with col2:
        seizures = st.checkbox("Seizures")
        cardiac = st.checkbox("Cardiac Issues")
    
    # Create patient data
    patient_data = {
        'age': age,
        'gender': 1 if gender == 'Male' else 0,
        'case_id': f"TEST_{datetime.now().strftime('%H%M%S')}",
        'seizures': 1 if seizures else 0,
        'cardiac_abnormalities': 1 if cardiac else 0
    }
    
    st.json(patient_data)
    
    # Emergency button
    if st.session_state.get('emergency_ready', False):
        st.markdown("---")
        st.subheader("🚨 Emergency Alert")
        
        # Simple emergency button
        if st.button("🚨 SEND EMERGENCY ALERT", type="primary", use_container_width=True):
            with st.spinner("🚨 Sending emergency alert..."):
                try:
                    success, message, alert = st.session_state.emergency_service.send_emergency_alert(
                        patient_data=patient_data,
                        urgency_level=UrgencyLevel.HIGH,
                        user_notes="Emergency from NGP main app test",
                        phone_number="+918319612060"
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.info("📱 Check your phone +91-831-961-2060 for SMS and voice call!")
                        
                        if alert:
                            st.json({
                                "Alert ID": alert.alert_id,
                                "SMS Content": alert.message_content,
                                "SMS SID": alert.message_sid,
                                "Call SID": alert.call_sid
                            })
                    else:
                        st.error(f"❌ {message}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        # Test button
        if st.button("🧪 Test SMS Only"):
            with st.spinner("Testing SMS..."):
                try:
                    success, message = st.session_state.emergency_service.test_sms_configuration("+918319612060")
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    else:
        st.error("❌ Emergency system not ready")

else:
    st.error("❌ Emergency system not available")

# Debug info
st.markdown("---")
st.subheader("🔧 Debug Info")
debug_info = {
    "Emergency Available": EMERGENCY_AVAILABLE,
    "Emergency Service": 'emergency_service' in st.session_state,
    "Emergency Ready": st.session_state.get('emergency_ready', False),
    "Session Keys": list(st.session_state.keys())
}
st.json(debug_info)