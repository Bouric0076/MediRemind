import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class BeemClient:
    """Client for interacting with Beem Africa's SMS and WhatsApp APIs"""
    
    def __init__(self):
        self.api_key = os.getenv("BEEM_API_KEY")
        self.secret_key = os.getenv("BEEM_SECRET_KEY")
        self.sender_id = os.getenv("BEEM_SENDER_ID", "MediRemind")  # Default sender ID
        self.whatsapp_template_namespace = os.getenv("BEEM_WHATSAPP_NAMESPACE")
        
        # API endpoints
        self.sms_url = "https://apisms.beem.africa/v1/send"
        self.whatsapp_url = "https://api.beem.africa/v1/whatsapp/send-template"
        
        if not all([self.api_key, self.secret_key]):
            raise ValueError("Beem API credentials not found in environment variables")
    
    def send_sms(self, recipient, message):
        """Send SMS using Beem Africa API"""
        try:
            payload = {
                "source_addr": self.sender_id,
                "schedule_time": "",
                "encoding": "0",
                "message": message,
                "recipients": [{"recipient_id": 1, "dest_addr": recipient}]
            }
            
            response = requests.post(
                self.sms_url,
                json=payload,
                auth=(self.api_key, self.secret_key),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                print(f"SMS sending failed: {response.text}")
                return False, response.text
                
            return True, "SMS sent successfully"
            
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False, str(e)
    
    def send_whatsapp(self, recipient, template_name, language_code="en", template_params=None):
        """Send WhatsApp message using Beem Africa API"""
        try:
            if not self.whatsapp_template_namespace:
                raise ValueError("WhatsApp template namespace not configured")
                
            payload = {
                "namespace": self.whatsapp_template_namespace,
                "template_name": template_name,
                "language": {"code": language_code},
                "to": recipient
            }
            
            # Add template parameters if provided
            if template_params:
                payload["parameters"] = template_params
            
            response = requests.post(
                self.whatsapp_url,
                json=payload,
                auth=(self.api_key, self.secret_key),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                print(f"WhatsApp message sending failed: {response.text}")
                return False, response.text
                
            return True, "WhatsApp message sent successfully"
            
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False, str(e)

# Create a singleton instance
beem_client = BeemClient()

__all__ = ['beem_client'] 