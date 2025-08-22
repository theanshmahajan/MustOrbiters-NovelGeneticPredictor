"""
Emergency Alert UI Components
Streamlit components for emergency alert system
"""

import streamlit as st
from typing import Dict, Optional, Tuple
from datetime import datetime

from .alert_service import EmergencyAlertService, UrgencyLevel
from .config_manager import ConfigurationManager

def render_emergency_button(patient_data: Dict, emergency_service: EmergencyAlertService, enabled: bool = True) -> bool:
    """
    Render emergency button component
    Returns True if emergency alert was triggered
    """
    
    # Check if patient data is available
    has_patient_data = bool(patient_data and any(patient_data.values()))
    button_enabled = enabled and has_patient_data
    
    # Custom CSS for emergency button
    st.markdown("""
    <style>
    .emergency-button {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(255, 68, 68, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        margin: 10px 0;
    }
    
    .emergency-button:hover {
        background: linear-gradient(135deg, #ff6666 0%, #ff0000 100%);
        box-shadow: 0 6px 12px rgba(255, 68, 68, 0.4);
        transform: translateY(-2px);
    }
    
    .emergency-button:disabled {
        background: #cccccc;
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
    }
    
    .emergency-status {
        background: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        border-left: 4px solid #ff4444;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Emergency button container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Button tooltip/status
        if not has_patient_data:
            st.markdown(
                '<div class="emergency-status">⚠️ Enter patient data to enable emergency alerts</div>',
                unsafe_allow_html=True
            )
        else:
            pass
            
        
        # Emergency button
        emergency_clicked = st.button(
            "🚨 EMERGENCY ALERT",
            key="emergency_button",
            disabled=not button_enabled,
            help="Send immediate SMS and voice call alert" if button_enabled else "Enter patient data first",
            use_container_width=True
        )
        
        if emergency_clicked and button_enabled:
            return True
    
    return False

def render_emergency_dialog(patient_data: Dict, emergency_service: EmergencyAlertService) -> Optional[Tuple[bool, str]]:
    """
    Render emergency alert dialog
    Returns (success, message) tuple if alert was sent, None otherwise
    """
    
    st.markdown("### 🚨 Emergency Alert Confirmation")
    st.markdown("---")
    
    # Patient context summary
    with st.expander("👤 Patient Context", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            age = patient_data.get('age', 'Unknown')
            gender = 'Male' if patient_data.get('gender') == 1 else 'Female' if patient_data.get('gender') == 0 else 'Unknown'
            st.write(f"**Age:** {age} years")
            st.write(f"**Gender:** {gender}")
            
        with col2:
            # Show key symptoms if present
            symptoms = []
            symptom_checks = [
                ('seizures', 'Seizures'),
                ('cardiac_abnormalities', 'Cardiac Issues'),
                ('respiratory_issues', 'Respiratory Issues'),
                ('developmental_delay', 'Developmental Delay'),
                ('intellectual_disability', 'Intellectual Disability')
            ]
            
            for symptom_key, symptom_name in symptom_checks:
                if patient_data.get(symptom_key) == 1:
                    symptoms.append(symptom_name)
            
            if symptoms:
                st.write("**Key Symptoms:**")
                for symptom in symptoms[:3]:  # Show max 3
                    st.write(f"• {symptom}")
            else:
                st.write("**Symptoms:** None selected")
    
    # Urgency level selection
    st.markdown("### ⚡ Urgency Level")
    urgency_options = {
        "Critical - Life threatening emergency": UrgencyLevel.CRITICAL,
        "High - Urgent medical attention needed": UrgencyLevel.HIGH,
        "Medium - Prompt medical review required": UrgencyLevel.MEDIUM,
        "Low - Non-urgent consultation needed": UrgencyLevel.LOW
    }
    
    selected_urgency_text = st.selectbox(
        "Select urgency level:",
        options=list(urgency_options.keys()),
        index=1  # Default to High
    )
    
    selected_urgency = urgency_options[selected_urgency_text]
    
    # Optional notes
    st.markdown("### 📝 Additional Notes (Optional)")
    user_notes = st.text_area(
        "Add any additional context or instructions:",
        placeholder="e.g., Patient showing signs of distress, family requesting immediate consultation...",
        max_chars=100
    )
    
    # Alert destination
    st.markdown("### 📱 Alert Destination")
    st.info("📞 SMS & Voice Call will be sent to: **+91 831-961-2060** (India)")
    
    # Confirmation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🚨 SEND EMERGENCY ALERT", type="primary", use_container_width=True):
            # Send the emergency alert
            with st.spinner("🚨 Sending emergency alert..."):
                success, message, alert = emergency_service.send_emergency_alert(
                    patient_data=patient_data,
                    urgency_level=selected_urgency,
                    user_notes=user_notes,
                    phone_number="+918319612060"
                )
                
                return success, message
    
    return None

def render_emergency_settings() -> None:
    """Render emergency system settings panel"""
    
    st.header("⚙️ Emergency Alert Settings")
    st.markdown("Configure Twilio credentials and emergency contacts")
    st.markdown("---")
    
    # Initialize config manager
    config_manager = ConfigurationManager()
    
    # Twilio Configuration Section
    st.subheader("📱 Twilio SMS/Voice Configuration")
    
    with st.expander("🔧 Twilio Account Settings", expanded=True):
        # Get current config
        current_config = config_manager.get_twilio_config()
        
        col1, col2 = st.columns(2)
        
        with col1:
            account_sid = st.text_input(
                "Account SID",
                value=current_config.account_sid if current_config else "",
                placeholder="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                help="Your Twilio Account SID from the Twilio Console"
            )
            
            from_number = st.text_input(
                "From Phone Number",
                value=current_config.from_phone_number if current_config else "",
                placeholder="+1234567890",
                help="Your Twilio phone number (must be verified)"
            )
        
        with col2:
            auth_token = st.text_input(
                "Auth Token",
                type="password",
                placeholder="Enter your Twilio Auth Token",
                help="Your Twilio Auth Token (kept secure with encryption)"
            )
            
            # Configuration status
            if current_config and current_config.is_configured:
                st.success("✅ Configured")
            else:
                st.warning("⚠️ Twilio not configured")
        
        # Save configuration
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("💾 Save Configuration", type="primary"):
                if account_sid and auth_token and from_number:
                    success = config_manager.save_twilio_config(
                        account_sid=account_sid,
                        auth_token=auth_token,
                        from_number=from_number
                    )
                    
                    if success:
                        st.success("✅ Configuration saved successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save configuration")
                else:
                    st.error("❌ Please fill in all required fields")
        
        with col2:
            if st.button("🧪 Test Configuration"):
                if current_config and current_config.is_configured:
                    # Initialize emergency service for testing
                    emergency_service = EmergencyAlertService(config_manager)
                    
                    with st.spinner("Testing SMS configuration..."):
                        success, message = emergency_service.test_sms_configuration("+918319612060")
                        
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.error("❌ Please configure Twilio settings first")
    
    # Emergency Contacts Section
    st.subheader("📞 Emergency Contacts")
    
    with st.expander("👥 Manage Emergency Contacts", expanded=True):
        # Current contacts
        contacts = config_manager.get_emergency_contacts()
        
        if contacts:
            st.write("**Current Emergency Contacts:**")
            for contact in contacts:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{contact.name}**")
                with col2:
                    st.write(contact.phone_number)
                with col3:
                    st.write(f"Priority: {contact.priority}")
        else:
            st.info("No emergency contacts configured")
        
        # Add new contact
        st.write("**Add New Emergency Contact:**")
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            new_name = st.text_input("Contact Name", placeholder="Dr. Smith")
        
        with col2:
            new_phone = st.text_input("Phone Number", placeholder="+1234567890")
        
        with col3:
            new_priority = st.number_input("Priority", min_value=1, max_value=10, value=1)
        
        if st.button("➕ Add Contact"):
            if new_name and new_phone:
                success = config_manager.add_emergency_contact(
                    name=new_name,
                    phone_number=new_phone,
                    priority=new_priority
                )
                
                if success:
                    st.success(f"✅ Added {new_name} to emergency contacts")
                    st.rerun()
                else:
                    st.error("❌ Failed to add contact (check phone number format)")
            else:
                st.error("❌ Please enter both name and phone number")
    
    # System Status
    st.subheader("📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if current_config and current_config.is_configured:
            st.metric("Twilio Status", "✅ Configured")
        else:
            st.metric("Twilio Status", "❌ Not Configured")
    
    with col2:
        contact_count = len(contacts)
        st.metric("Emergency Contacts", f"{contact_count}")
    
    with col3:
        st.metric("Target Phone", "+91-831-961-2060")