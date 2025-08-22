"""
Configuration Manager for Emergency Alert System
Handles secure storage and retrieval of Twilio credentials and emergency contacts
"""

import os
import json
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TwilioConfig:
    account_sid: str
    auth_token: str
    from_phone_number: str
    is_configured: bool = False
    last_tested: Optional[datetime] = None

@dataclass
class EmergencyContact:
    contact_id: str
    name: str
    phone_number: str
    priority: int = 1
    is_active: bool = True
    created_date: Optional[datetime] = None

class ConfigurationManager:
    """Manages secure configuration for emergency alert system"""
    
    def __init__(self, config_dir: str = "emergency/config"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "emergency_config.json")
        self.key_file = os.path.join(config_dir, "encryption.key")
        
        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        
        # Initialize encryption
        self.cipher = self._get_or_create_cipher()
    
    def _get_or_create_cipher(self) -> Fernet:
        """Get or create encryption cipher"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        return Fernet(key)
    
    def save_twilio_config(self, account_sid: str, auth_token: str, from_number: str) -> bool:
        """Save Twilio configuration with encryption"""
        try:
            config = self._load_config()
            
            # Encrypt sensitive data
            encrypted_token = self.cipher.encrypt(auth_token.encode()).decode()
            
            config['twilio'] = {
                'account_sid': account_sid,
                'auth_token': encrypted_token,
                'from_phone_number': from_number,
                'is_configured': True,
                'last_updated': datetime.now().isoformat()
            }
            
            self._save_config(config)
            return True
            
        except Exception as e:
            print(f"Error saving Twilio config: {e}")
            return False
    
    def get_twilio_config(self) -> Optional[TwilioConfig]:
        """Get Twilio configuration with decryption"""
        try:
            config = self._load_config()
            twilio_config = config.get('twilio', {})
            
            if not twilio_config.get('is_configured', False):
                return None
            
            # Decrypt auth token
            encrypted_token = twilio_config.get('auth_token', '')
            auth_token = self.cipher.decrypt(encrypted_token.encode()).decode()
            
            return TwilioConfig(
                account_sid=twilio_config.get('account_sid', ''),
                auth_token=auth_token,
                from_phone_number=twilio_config.get('from_phone_number', ''),
                is_configured=True,
                last_tested=datetime.fromisoformat(twilio_config.get('last_tested', datetime.now().isoformat()))
            )
            
        except Exception as e:
            print(f"Error loading Twilio config: {e}")
            return None
    
    def add_emergency_contact(self, name: str, phone_number: str, priority: int = 1) -> bool:
        """Add emergency contact"""
        try:
            if not self.validate_phone_number(phone_number):
                return False
            
            config = self._load_config()
            contacts = config.get('emergency_contacts', [])
            
            contact = {
                'contact_id': f"contact_{len(contacts) + 1}",
                'name': name,
                'phone_number': phone_number,
                'priority': priority,
                'is_active': True,
                'created_date': datetime.now().isoformat()
            }
            
            contacts.append(contact)
            config['emergency_contacts'] = contacts
            
            self._save_config(config)
            return True
            
        except Exception as e:
            print(f"Error adding emergency contact: {e}")
            return False
    
    def get_emergency_contacts(self) -> List[EmergencyContact]:
        """Get all active emergency contacts"""
        try:
            config = self._load_config()
            contacts_data = config.get('emergency_contacts', [])
            
            contacts = []
            for contact_data in contacts_data:
                if contact_data.get('is_active', True):
                    contact = EmergencyContact(
                        contact_id=contact_data.get('contact_id', ''),
                        name=contact_data.get('name', ''),
                        phone_number=contact_data.get('phone_number', ''),
                        priority=contact_data.get('priority', 1),
                        is_active=contact_data.get('is_active', True),
                        created_date=datetime.fromisoformat(contact_data.get('created_date', datetime.now().isoformat()))
                    )
                    contacts.append(contact)
            
            return sorted(contacts, key=lambda x: x.priority)
            
        except Exception as e:
            print(f"Error loading emergency contacts: {e}")
            return []
    
    def validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format"""
        import re
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone_number)
        
        # Check if it's a valid US phone number (10 or 11 digits)
        if len(digits_only) == 10:
            return True
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return True
        
        return False
    
    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number to E.164 format"""
        import re
        
        digits_only = re.sub(r'\D', '', phone_number)
        
        if len(digits_only) == 10:
            return f"+1{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"
        
        return phone_number
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return {}
    
    def _save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)