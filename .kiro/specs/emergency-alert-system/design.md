# Design Document

## Overview

The Emergency Alert System is a critical safety feature that integrates SMS notification capabilities into the Novel Genetic Predictor application. The system leverages Twilio's SMS API to send real-time alerts to healthcare personnel when emergency situations arise during patient diagnosis. The design emphasizes reliability, security, and ease of use while maintaining HIPAA compliance considerations for patient data handling.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Emergency      │    │   Twilio SMS    │
│   Frontend      │───▶│   Alert Service  │───▶│   API Service   │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌──────────────────┐             │
         │              │   Configuration  │             │
         └─────────────▶│   Manager        │             │
                        │                  │             │
                        └──────────────────┘             │
                                 │                       │
                                 ▼                       │
                        ┌──────────────────┐             │
                        │   Alert History  │             │
                        │   Database       │             │
                        │                  │             │
                        └──────────────────┘             │
                                                         │
                        ┌──────────────────┐             │
                        │   Healthcare     │◀────────────┘
                        │   Personnel      │
                        │   Mobile Device  │
                        └──────────────────┘
```

### Component Interaction Flow

1. **User Trigger**: Healthcare professional clicks emergency button in Patient Diagnosis interface
2. **Context Capture**: System captures current patient data and diagnosis state
3. **Alert Dialog**: User selects urgency level and confirms emergency alert
4. **Message Generation**: System formats SMS message with patient context and urgency
5. **SMS Delivery**: Twilio API sends SMS to configured emergency contacts
6. **Confirmation**: System displays delivery confirmation and logs the event
7. **History Tracking**: Alert details stored for audit and reporting purposes

## Components and Interfaces

### 1. Emergency Alert Service (`emergency_alert.py`)

**Purpose**: Core service handling SMS alert logic and Twilio integration

**Key Methods**:
```python
class EmergencyAlertService:
    def __init__(self, config_manager)
    def send_emergency_alert(patient_data, urgency_level, user_notes="")
    def format_emergency_message(patient_data, urgency_level, user_notes)
    def validate_phone_number(phone_number)
    def test_sms_configuration()
    def get_delivery_status(message_sid)
```

**Interfaces**:
- Input: Patient data dictionary, urgency level enum, optional user notes
- Output: SMS delivery status, message SID, timestamp
- External: Twilio REST API for SMS delivery

### 2. Configuration Manager (`config_manager.py`)

**Purpose**: Secure storage and retrieval of Twilio credentials and emergency contacts

**Key Methods**:
```python
class ConfigurationManager:
    def __init__(self)
    def save_twilio_config(account_sid, auth_token, from_number)
    def get_twilio_config()
    def add_emergency_contact(name, phone_number, priority)
    def get_emergency_contacts()
    def encrypt_credentials(data)
    def decrypt_credentials(encrypted_data)
```

**Security Features**:
- AES encryption for sensitive credentials
- Environment variable fallback for production
- Input validation and sanitization
- Secure credential storage in local config files

### 3. Alert History Manager (`alert_history.py`)

**Purpose**: Logging and retrieval of emergency alert events for audit purposes

**Key Methods**:
```python
class AlertHistoryManager:
    def __init__(self)
    def log_emergency_alert(alert_data)
    def get_alert_history(date_range=None, urgency_filter=None)
    def export_alert_history(format="csv")
    def get_alert_statistics()
```

**Data Storage**:
- SQLite database for local storage
- JSON format for alert event data
- Automatic cleanup of old records (90+ days)
- Export capabilities for compliance reporting

### 4. Emergency UI Components

**Emergency Button Component**:
```python
def render_emergency_button(patient_data, enabled=True):
    # Red emergency button with icon
    # Tooltip showing current status
    # Click handler for emergency dialog
```

**Emergency Dialog Component**:
```python
def render_emergency_dialog(patient_data):
    # Urgency level selection (Low, Medium, High, Critical)
    # Optional notes text area
    # Patient context summary
    # Confirm/Cancel buttons
```

**Settings Panel Component**:
```python
def render_emergency_settings():
    # Twilio configuration fields
    # Emergency contacts management
    # Test SMS functionality
    # Configuration validation
```

## Data Models

### Emergency Alert Event
```python
@dataclass
class EmergencyAlert:
    alert_id: str
    timestamp: datetime
    patient_case_id: str
    urgency_level: UrgencyLevel
    message_content: str
    recipient_phone: str
    delivery_status: DeliveryStatus
    message_sid: str
    user_notes: str
    patient_context: dict
```

### Twilio Configuration
```python
@dataclass
class TwilioConfig:
    account_sid: str
    auth_token: str  # Encrypted
    from_phone_number: str
    is_configured: bool
    last_tested: datetime
```

### Emergency Contact
```python
@dataclass
class EmergencyContact:
    contact_id: str
    name: str
    phone_number: str
    priority: int
    is_active: bool
    created_date: datetime
```

## Error Handling

### SMS Delivery Failures
- **Network Issues**: Retry mechanism with exponential backoff (3 attempts)
- **Invalid Phone Numbers**: Immediate validation with user feedback
- **Twilio API Errors**: Specific error messages with troubleshooting guidance
- **Rate Limiting**: Queue management and user notification of delays

### Configuration Errors
- **Missing Credentials**: Clear setup instructions with validation steps
- **Invalid Credentials**: Test functionality with detailed error reporting
- **Encryption Failures**: Fallback to environment variables with security warnings

### Data Validation
- **Patient Data**: Graceful handling of missing or invalid patient information
- **Phone Number Format**: International format validation with auto-correction
- **Message Length**: Automatic truncation with priority content preservation

## Testing Strategy

### Unit Tests
```python
# Test SMS message formatting
def test_format_emergency_message():
    # Test various patient data scenarios
    # Test urgency level formatting
    # Test message length limits

# Test configuration management
def test_twilio_config_encryption():
    # Test credential encryption/decryption
    # Test configuration validation
    # Test secure storage

# Test phone number validation
def test_phone_number_validation():
    # Test various phone number formats
    # Test international numbers
    # Test invalid inputs
```

### Integration Tests
```python
# Test Twilio API integration
def test_twilio_sms_delivery():
    # Test successful SMS delivery
    # Test API error handling
    # Test delivery status tracking

# Test end-to-end emergency flow
def test_emergency_alert_flow():
    # Test button click to SMS delivery
    # Test patient context capture
    # Test alert history logging
```

### User Acceptance Tests
- **Emergency Button Accessibility**: Verify button visibility and click responsiveness
- **SMS Delivery Speed**: Confirm sub-10-second delivery times
- **Message Content Accuracy**: Validate patient information in SMS messages
- **Configuration Workflow**: Test complete setup process for new users
- **Error Recovery**: Test system behavior during various failure scenarios

### Security Tests
- **Credential Protection**: Verify encryption of sensitive Twilio credentials
- **Patient Data Privacy**: Ensure minimal PHI exposure in SMS messages
- **Access Control**: Test unauthorized access prevention
- **Audit Trail**: Verify complete logging of emergency events

## Performance Considerations

### SMS Delivery Optimization
- **Async Processing**: Non-blocking SMS delivery to maintain UI responsiveness
- **Connection Pooling**: Reuse Twilio API connections for better performance
- **Caching**: Cache Twilio client instances and configuration data
- **Batch Processing**: Support for multiple emergency contacts (future enhancement)

### UI Responsiveness
- **Progressive Loading**: Show immediate feedback while processing emergency alerts
- **Error Boundaries**: Prevent emergency system failures from crashing main application
- **State Management**: Maintain patient context during emergency alert process
- **Memory Management**: Efficient handling of alert history data

## Security Implementation

### Credential Management
```python
# AES encryption for Twilio credentials
from cryptography.fernet import Fernet

class SecureCredentialManager:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_credential(self, credential):
        return self.cipher.encrypt(credential.encode())
    
    def decrypt_credential(self, encrypted_credential):
        return self.cipher.decrypt(encrypted_credential).decode()
```

### Patient Data Protection
- **Minimal Data Exposure**: Include only essential patient information in SMS
- **Data Anonymization**: Use case IDs instead of patient names when possible
- **Secure Transmission**: Leverage Twilio's encrypted SMS delivery
- **Audit Logging**: Track all emergency alert events for compliance

### Access Control
- **Configuration Protection**: Restrict emergency settings to authorized users
- **Button Access Control**: Enable emergency button only for valid patient cases
- **Credential Validation**: Verify Twilio credentials before allowing configuration save
- **Session Management**: Ensure emergency alerts are tied to active user sessions