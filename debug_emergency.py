#!/usr/bin/env python3
"""
Debug Emergency System in Streamlit
Simple test to check if emergency button works in Streamlit
"""

import streamlit as st
from datetime import datetime

# Import emergency system
try:
    from emergency.config_manager import ConfigurationManager
    from emergency.alert_service import EmergencyAlertService, UrgencyLevel
    from emergency.ui_components import render_emergency_button, render_emergency_dialog
    EMERGENCY_SYSTEM_AVAILABLE = True
    st.success("✅ Emergency system loaded successfully")
except ImportError as e:
    st.error(f"❌ Emergency system not available: {e}")
    EMERGENCY_SYSTEM_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Emergency System Debug",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Emergency System Debug Test")
st.markdown("Testing emergency button functionality for +91-831-961-2060")

# Initialize session state
if 'emergency_service' not in st.session_state and EMERGENCY_SYSTEM_AVAILABLE:
    try:
        config_manager = ConfigurationManager()
        st.session_state.emergency_service = EmergencyAlertService(config_manager)
        st.success("✅ Emergency service initialized")
    except Exception as e:
        st.error(f"❌ Failed to initialize emergency service: {e}")
        EMERGENCY_SYSTEM_AVAILABLE = False

if 'show_emergency_dialog' not in st.session_state:
    st.session_state.show_emergency_dialog = False

if 'current_patient_data' not in st.session_state:
    st.session_state.current_patient_data = {}

# Check Twilio configuration
if EMERGENCY_SYSTEM_AVAILABLE:
    config_manager = ConfigurationManager()
    twilio_config = config_manager.get_twilio_config()
    
    if twilio_config and twilio_config.is_configured:
        st.success("✅ Twilio configuration found")
        st.info(f"📱 From Number: {twilio_config.from_phone_number}")
        st.info(f"🎯 Target: +91-831-961-2060")
    else:
        st.error("❌ Twilio not configured. Run configure_india.py first.")
        st.stop()

# Emergency Alert Dialog
if EMERGENCY_SYSTEM_AVAILABLE and st.session_state.get('show_emergency_dialog', False):
    st.markdown("---")
    st.subheader("🚨 Emergency Alert Dialog")
    
    with st.container():
        result = render_emergency_dialog(st.session_state.current_patient_data, st.session_state.emergency_service)
        if result is not None:
            success, message = result
            if success:
                st.success(f"✅ {message}")
                st.balloons()
            else:
                st.error(f"❌ {message}")
            st.session_state.show_emergency_dialog = False
            st.rerun()

# Sample patient data form
st.markdown("---")
st.subheader("👤 Sample Patient Data")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age (years)", 0, 18, 5)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    seizures = st.checkbox("Seizures")
    cardiac_issues = st.checkbox("Cardiac Issues")

# Create patient data
patient_data = {
    'age': age,
    'gender': 1 if gender == 'Male' else 0,
    'case_id': f"DEBUG_{datetime.now().strftime('%H%M%S')}",
    'seizures': 1 if seizures else 0,
    'cardiac_abnormalities': 1 if cardiac_issues else 0,
    'height_cm': 120,
    'weight_kg': 25,
    'bp_systolic': 100,
    'bp_diastolic': 70
}

st.session_state.current_patient_data = patient_data.copy()

# Display current patient data
st.markdown("---")
st.subheader("📋 Current Patient Data")
st.json(patient_data)

# Emergency button test
st.markdown("---")
st.subheader("🚨 Emergency Button Test")

if EMERGENCY_SYSTEM_AVAILABLE:
    # Manual emergency button (simplified version)
    if st.button("🚨 TEST EMERGENCY ALERT", type="primary", use_container_width=True):
        st.session_state.show_emergency_dialog = True
        st.rerun()
    
    # Direct test button (bypasses dialog)
    if st.button("⚡ DIRECT SMS + CALL TEST", use_container_width=True):
        with st.spinner("🚨 Sending emergency alert directly..."):
            try:
                success, message, alert = st.session_state.emergency_service.send_emergency_alert(
                    patient_data=patient_data,
                    urgency_level=UrgencyLevel.HIGH,
                    user_notes="Direct test from Streamlit debug",
                    phone_number="+918319612060"
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.info("📱 Check your phone +91-831-961-2060 for SMS and voice call!")
                    
                    if alert:
                        st.json({
                            "Alert ID": alert.alert_id,
                            "Timestamp": str(alert.timestamp),
                            "Urgency": alert.urgency_level.value,
                            "SMS Content": alert.message_content,
                            "SMS SID": alert.message_sid,
                            "Call SID": alert.call_sid
                        })
                else:
                    st.error(f"❌ {message}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Component test button (uses UI component)
    st.markdown("### 🧪 Component Test")
    emergency_clicked = render_emergency_button(
        patient_data=patient_data,
        emergency_service=st.session_state.emergency_service,
        enabled=True
    )
    
    if emergency_clicked:
        st.success("✅ Emergency button clicked!")
        st.session_state.show_emergency_dialog = True
        st.rerun()

else:
    st.error("❌ Emergency system not available")

# Debug information
st.markdown("---")
st.subheader("🔧 Debug Information")

debug_info = {
    "Emergency System Available": EMERGENCY_SYSTEM_AVAILABLE,
    "Emergency Service Initialized": 'emergency_service' in st.session_state,
    "Show Dialog": st.session_state.get('show_emergency_dialog', False),
    "Patient Data Available": bool(st.session_state.current_patient_data),
    "Session State Keys": list(st.session_state.keys())
}

st.json(debug_info)

# Instructions
st.markdown("---")
st.subheader("📖 Instructions")
st.markdown("""
1. **TEST EMERGENCY ALERT**: Opens the emergency dialog (like in main app)
2. **DIRECT SMS + CALL TEST**: Sends SMS and voice call immediately
3. **Component Test**: Tests the emergency button component

**Expected Result**: You should receive SMS and voice call on +91-831-961-2060

**If it doesn't work**:
- Check if Twilio is configured (run `python configure_india.py`)
- Check debug information below
- Look at console output for errors
""")