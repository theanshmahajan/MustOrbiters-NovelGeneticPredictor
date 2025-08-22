"""
Emergency Alert Service
Handles SMS and voice call alerts via Twilio API
"""

import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio not installed. Install with: pip install twilio")

from .config_manager import ConfigurationManager, TwilioConfig

class UrgencyLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class DeliveryStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    UNDELIVERED = "undelivered"

@dataclass
class EmergencyAlert:
    alert_id: str
    timestamp: datetime
    patient_case_id: str
    urgency_level: UrgencyLevel
    message_content: str
    recipient_phone: str
    delivery_status: DeliveryStatus
    message_sid: Optional[str] = None
    call_sid: Optional[str] = None
    user_notes: str = ""
    patient_context: Optional[Dict] = None

class EmergencyAlertService:
    """Core service for emergency SMS and voice alerts"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.twilio_client = None
        self.alert_history = []
        
        # Initialize Twilio client
        self._initialize_twilio_client()
    
    def _initialize_twilio_client(self) -> bool:
        """Initialize Twilio client with stored configuration"""
        if not TWILIO_AVAILABLE:
            print("❌ Twilio library not available")
            return False
        
        try:
            twilio_config = self.config_manager.get_twilio_config()
            if twilio_config and twilio_config.is_configured:
                self.twilio_client = Client(
                    twilio_config.account_sid,
                    twilio_config.auth_token
                )
                print("✅ Twilio client initialized successfully")
                return True
            else:
                print("⚠️ Twilio not configured")
                return False
                
        except Exception as e:
            print(f"❌ Error initializing Twilio client: {e}")
            return False
    
    def send_emergency_alert(self, patient_data: Dict, urgency_level: UrgencyLevel, 
                           user_notes: str = "", phone_number: str = "+918319612060") -> Tuple[bool, str, Optional[EmergencyAlert]]:
        """Send emergency SMS and voice call alert"""
        
        if not self.twilio_client:
            if not self._initialize_twilio_client():
                return False, "Twilio client not available", None
        
        try:
            # Generate alert ID
            alert_id = f"EMRG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Format SMS message
            sms_message = self._format_emergency_message(patient_data, urgency_level, user_notes)
            
            # Get Twilio config
            twilio_config = self.config_manager.get_twilio_config()
            if not twilio_config:
                return False, "Twilio configuration not found", None
            
            # Send SMS
            sms_result = self._send_sms(
                to_number=phone_number,
                message=sms_message,
                from_number=twilio_config.from_phone_number
            )
            
            # Send Voice Call
            voice_result = self._make_voice_call(
                to_number=phone_number,
                urgency_level=urgency_level,
                patient_data=patient_data,
                from_number=twilio_config.from_phone_number
            )
            
            # Create alert record
            alert = EmergencyAlert(
                alert_id=alert_id,
                timestamp=datetime.now(),
                patient_case_id=patient_data.get('case_id', f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                urgency_level=urgency_level,
                message_content=sms_message,
                recipient_phone=phone_number,
                delivery_status=DeliveryStatus.SENT if sms_result[0] else DeliveryStatus.FAILED,
                message_sid=sms_result[1] if sms_result[0] else None,
                call_sid=voice_result[1] if voice_result[0] else None,
                user_notes=user_notes,
                patient_context=patient_data.copy()
            )
            
            # Store in history
            self.alert_history.append(alert)
            
            if sms_result[0] and voice_result[0]:
                return True, f"✅ Emergency alert sent successfully! ", alert
            elif sms_result[0]:
                return True, f"⚠️ SMS sent successfully", alert
            elif voice_result[0]:
                return True, f"⚠️ Voice call initiated successfully", alert
            else:
                return False, f"❌ Both SMS and voice call failed", alert
                
        except Exception as e:
            error_msg = f"❌ Emergency alert failed: {str(e)}"
            print(error_msg)
            return False, error_msg, None
    
    def _send_sms(self, to_number: str, message: str, from_number: str) -> Tuple[bool, str]:
        """Send SMS message via Twilio"""
        try:
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            return True, message_obj.sid
            
        except TwilioException as e:
            return False, f"Twilio SMS error: {str(e)}"
        except Exception as e:
            return False, f"SMS error: {str(e)}"
    
    def _make_voice_call(self, to_number: str, urgency_level: UrgencyLevel, 
                        patient_data: Dict, from_number: str) -> Tuple[bool, str]:
        """Make voice call via Twilio"""
        try:
            # Create TwiML for voice message
            twiml_message = self._generate_voice_message(urgency_level, patient_data)
            
            # Create call
            call = self.twilio_client.calls.create(
                twiml=twiml_message,
                to=to_number,
                from_=from_number
            )
            return True, call.sid
            
        except TwilioException as e:
            return False, f"Twilio voice call error: {str(e)}"
        except Exception as e:
            return False, f"Voice call error: {str(e)}"
    
    def _generate_voice_message(self, urgency_level: UrgencyLevel, patient_data: Dict) -> str:
        """Generate TwiML for voice message"""
        age = patient_data.get('age', 'unknown')
        gender = 'male' if patient_data.get('gender') == 1 else 'female'
        
        urgency_text = {
            UrgencyLevel.CRITICAL: "CRITICAL EMERGENCY",
            UrgencyLevel.HIGH: "HIGH PRIORITY EMERGENCY",
            UrgencyLevel.MEDIUM: "MEDIUM PRIORITY ALERT",
            UrgencyLevel.LOW: "LOW PRIORITY ALERT"
        }.get(urgency_level, "EMERGENCY ALERT")
        
        message = f"""
        <Response>
            <Say voice="alice">
                {urgency_text} from Novel Genetic Predictor system.
                Emergency alert for {age} year old {gender} patient.
                Please check your SMS for detailed information.
                This message will repeat once.
            </Say>
            <Pause length="2"/>
            <Say voice="alice">
                {urgency_text} from Novel Genetic Predictor system.
                Emergency alert for {age} year old {gender} patient.
                Please check your SMS for detailed information.
            </Say>
        </Response>
        """
        
        return message.strip()
    
    def _format_emergency_message(self, patient_data: Dict, urgency_level: UrgencyLevel, user_notes: str = "") -> str:
        """Format emergency SMS message with patient context"""
        
        # Get basic patient info
        age = patient_data.get('age', 'Unknown')
        gender = 'Male' if patient_data.get('gender') == 1 else 'Female' if patient_data.get('gender') == 0 else 'Unknown'
        case_id = patient_data.get('case_id', f"CASE_{datetime.now().strftime('%H%M%S')}")
        
        # Urgency prefix
        urgency_prefixes = {
            UrgencyLevel.CRITICAL: "🚨 CRITICAL EMERGENCY",
            UrgencyLevel.HIGH: "⚠️ HIGH PRIORITY",
            UrgencyLevel.MEDIUM: "📋 MEDIUM PRIORITY", 
            UrgencyLevel.LOW: "ℹ️ LOW PRIORITY"
        }
        
        urgency_prefix = urgency_prefixes.get(urgency_level, "🚨 EMERGENCY")
        
        # Build message
        message_parts = [
            f"{urgency_prefix} - NGP Alert",
            f"Patient: {age}yr {gender}",
            f"Case: {case_id}",
        ]
        
        # Add key symptoms if present
        key_symptoms = []
        symptom_checks = [
            ('seizures', 'Seizures'),
            ('cardiac_abnormalities', 'Cardiac issues'),
            ('respiratory_issues', 'Respiratory issues'),
            ('developmental_delay', 'Dev delay'),
            ('intellectual_disability', 'Intellectual disability'),
            ('failure_to_thrive', 'Failure to thrive')
        ]
        
        for symptom_key, symptom_name in symptom_checks:
            if patient_data.get(symptom_key) == 1:
                key_symptoms.append(symptom_name)
        
        if key_symptoms:
            symptoms_text = ", ".join(key_symptoms[:3])  # Max 3 symptoms
            message_parts.append(f"Symptoms: {symptoms_text}")
        
        # Add user notes if provided
        if user_notes.strip():
            message_parts.append(f"Notes: {user_notes.strip()[:50]}")  # Limit notes length
        
        # Add timestamp and callback instruction
        timestamp = datetime.now().strftime("%H:%M")
        message_parts.extend([
            f"Time: {timestamp}",
            "Please respond ASAP"
        ])
        
        # Join message parts
        message = " | ".join(message_parts)
        
        # Ensure message is within SMS limits (160 characters for single SMS)
        if len(message) > 160:
            # Truncate while preserving critical info
            essential_parts = [
                f"{urgency_prefix}",
                f"Patient: {age}yr {gender}",
                f"Case: {case_id}",
                f"Time: {timestamp}",
                "Check NGP system"
            ]
            message = " | ".join(essential_parts)
        
        return message
    
    def test_sms_configuration(self, test_phone_number: str = "+918319612060") -> Tuple[bool, str]:
        """Test SMS configuration by sending a test message"""
        if not self.twilio_client:
            if not self._initialize_twilio_client():
                return False, "Twilio client not available"
        
        try:
            twilio_config = self.config_manager.get_twilio_config()
            if not twilio_config:
                return False, "Twilio configuration not found"
            
            test_message = f"🧬 NGP Emergency System Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Configuration working correctly!"
            
            result = self._send_sms(
                to_number=test_phone_number,
                message=test_message,
                from_number=twilio_config.from_phone_number
            )
            
            if result[0]:
                return True, f" Test SMS sent successfully! "
            else:
                return False, f"❌ Test SMS failed: {result[1]}"
                
        except Exception as e:
            return False, f"❌ Test failed: {str(e)}"
    
    def get_alert_history(self) -> List[EmergencyAlert]:
        """Get emergency alert history"""
        return self.alert_history.copy()
    
    def get_delivery_status(self, message_sid: str) -> Optional[str]:
        """Get delivery status for a specific message"""
        if not self.twilio_client:
            return None
        
        try:
            message = self.twilio_client.messages(message_sid).fetch()
            return message.status
        except Exception as e:
            print(f"Error fetching delivery status: {e}")
            return None