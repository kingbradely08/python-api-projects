#!/usr/bin/env python3
"""
Email & SMS Notification System
Send automated notifications via email and SMS
APIs: SendGrid (email), Twilio (SMS)
"""

import os
from dotenv import load_dotenv
import argparse
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class NotificationSystem:
    def __init__(self):
        # SendGrid configuration
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL')
        
        # Twilio configuration
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        self.email_enabled = bool(self.sendgrid_key and self.from_email)
        self.sms_enabled = bool(self.twilio_sid and self.twilio_token and self.twilio_number)
        
        if self.email_enabled:
            print("✅ Email notifications enabled (SendGrid)")
        else:
            print("⚠️  Email notifications disabled (missing SendGrid config)")
        
        if self.sms_enabled:
            print("✅ SMS notifications enabled (Twilio)")
        else:
            print("⚠️  SMS notifications disabled (missing Twilio config)")
    
    def send_email(self, to_email, subject, content, content_type='text/plain'):
        """Send email using SendGrid"""
        if not self.email_enabled:
            print("❌ Email not configured!")
            return False
        
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Content
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content if content_type == 'text/plain' else None,
                html_content=content if content_type == 'text/html' else None
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Email sent to {to_email}")
                print(f"   Subject: {subject}")
                return True
            else:
                print(f"❌ Email failed: Status {response.status_code}")
                return False
                
        except ImportError:
            print("❌ SendGrid library not installed!")
            print("   Install: pip install sendgrid")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_sms(self, to_number, message):
        """Send SMS using Twilio"""
        if not self.sms_enabled:
            print("❌ SMS not configured!")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_sid, self.twilio_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=self.twilio_number,
                to=to_number
            )
            
            print(f"✅ SMS sent to {to_number}")
            print(f"   Message SID: {message_obj.sid}")
            return True
            
        except ImportError:
            print("❌ Twilio library not installed!")
            print("   Install: pip install twilio")
            return False
        except Exception as e:
            print(f"❌ Error sending SMS: {e}")
            return False
    
    def send_bulk_email(self, recipients, subject, content, content_type='text/plain'):
        """Send email to multiple recipients"""
        if not self.email_enabled:
            print("❌ Email not configured!")
            return
        
        print(f"📧 Sending bulk email to {len(recipients)} recipient(s)...")
        
        success_count = 0
        fail_count = 0
        
        for recipient in recipients:
            if self.send_email(recipient, subject, content, content_type):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n📊 Results: {success_count} sent, {fail_count} failed")
    
    def send_bulk_sms(self, recipients, message):
        """Send SMS to multiple recipients"""
        if not self.sms_enabled:
            print("❌ SMS not configured!")
            return
        
        print(f"📱 Sending bulk SMS to {len(recipients)} recipient(s)...")
        
        success_count = 0
        fail_count = 0
        
        for recipient in recipients:
            if self.send_sms(recipient, message):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n📊 Results: {success_count} sent, {fail_count} failed")
    
    def send_notification(self, recipient, message, channel='email', subject=None):
        """Send notification via specified channel"""
        if channel == 'email':
            if not subject:
                subject = "Notification"
            return self.send_email(recipient, subject, message)
        elif channel == 'sms':
            return self.send_sms(recipient, message)
        elif channel == 'both':
            email_success = self.send_email(recipient, subject or "Notification", message)
            sms_success = self.send_sms(recipient, message)
            return email_success or sms_success
        else:
            print(f"❌ Invalid channel: {channel}")
            return False
    
    def validate_email(self, email):
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Basic phone validation"""
        import re
        # Remove spaces, dashes, parentheses
        clean = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it's a valid format (starts with + and has 10-15 digits)
        return re.match(r'^\+?[1-9]\d{9,14}$', clean) is not None
    
    def load_template(self, template_name):
        """Load email template from file"""
        template_file = f"templates/{template_name}.html"
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ Template not found: {template_file}")
            return None
        except Exception as e:
            print(f"❌ Error loading template: {e}")
            return None
    
    def format_template(self, template, **kwargs):
        """Format template with variables"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"❌ Missing template variable: {e}")
            return None
    
    def schedule_notification(self, recipient, message, channel, send_time):
        """Schedule notification for later (saves to file)"""
        scheduled = {
            'recipient': recipient,
            'message': message,
            'channel': channel,
            'send_time': send_time,
            'created_at': datetime.now().isoformat()
        }
        
        # Save to scheduled notifications file
        schedule_file = 'scheduled_notifications.json'
        
        try:
            # Load existing schedule
            if os.path.exists(schedule_file):
                with open(schedule_file, 'r') as f:
                    schedule = json.load(f)
            else:
                schedule = []
            
            # Add new notification
            schedule.append(scheduled)
            
            # Save updated schedule
            with open(schedule_file, 'w') as f:
                json.dump(schedule, f, indent=2)
            
            print(f"⏰ Notification scheduled for {send_time}")
            print(f"   Saved to {schedule_file}")
            
        except Exception as e:
            print(f"❌ Error scheduling notification: {e}")
    
    def load_contacts(self, filename):
        """Load contacts from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
            print(f"📇 Loaded {len(contacts)} contact(s)")
            return contacts
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return []
        except Exception as e:
            print(f"❌ Error loading contacts: {e}")
            return []
    
    def send_test_notifications(self):
        """Send test notifications"""
        print("\n🧪 Testing Notification System...\n")
        
        # Test email
        if self.email_enabled:
            test_email = input("Enter email for test (or press Enter to skip): ").strip()
            if test_email:
                self.send_email(
                    test_email,
                    "Test Email from Notification System",
                    "This is a test email. If you received this, email notifications are working!"
                )
        
        # Test SMS
        if self.sms_enabled:
            test_phone = input("Enter phone number for test (or press Enter to skip): ").strip()
            if test_phone:
                self.send_sms(
                    test_phone,
                    "Test SMS from Notification System. SMS notifications are working!"
                )


def create_sample_html_template():
    """Create a sample HTML email template"""
    template = """<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background: #f4f4f4; }}
        .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            <p>{message}</p>
        </div>
        <div class="footer">
            <p>Sent by Notification System | {date}</p>
        </div>
    </div>
</body>
</html>"""
    
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Save template
    with open('templates/default.html', 'w') as f:
        f.write(template)
    
    print("✅ Sample template created: templates/default.html")


def main():
    parser = argparse.ArgumentParser(
        description='Email & SMS Notification System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python notifier.py --email user@example.com --subject "Hello" --message "Test"
  python notifier.py --sms +1234567890 --message "Alert!"
  python notifier.py --bulk-email emails.json --subject "News" --message "Update"
  python notifier.py --test
  python notifier.py --create-template
        """
    )
    
    parser.add_argument('--email', metavar='EMAIL', help='Send email to address')
    parser.add_argument('--sms', metavar='PHONE', help='Send SMS to phone number')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--message', help='Message content')
    parser.add_argument('--html', action='store_true', help='Send as HTML email')
    
    parser.add_argument('--bulk-email', metavar='FILE', help='Send bulk emails (JSON file with list of emails)')
    parser.add_argument('--bulk-sms', metavar='FILE', help='Send bulk SMS (JSON file with list of phones)')
    
    parser.add_argument('--template', metavar='NAME', help='Use email template')
    parser.add_argument('--template-vars', metavar='JSON', help='Template variables as JSON')
    
    parser.add_argument('--test', action='store_true', help='Send test notifications')
    parser.add_argument('--create-template', action='store_true', help='Create sample HTML template')
    
    args = parser.parse_args()
    
    notifier = NotificationSystem()
    
    if args.create_template:
        create_sample_html_template()
        return
    
    if args.test:
        notifier.send_test_notifications()
        return
    
    # Handle template
    message = args.message
    content_type = 'text/html' if args.html else 'text/plain'
    
    if args.template:
        template_content = notifier.load_template(args.template)
        if template_content and args.template_vars:
            try:
                vars_dict = json.loads(args.template_vars)
                message = notifier.format_template(template_content, **vars_dict)
                content_type = 'text/html'
            except json.JSONDecodeError:
                print("❌ Invalid JSON for template variables")
                return
    
    # Send individual notifications
    if args.email:
        if not message:
            print("❌ Please provide --message")
            return
        if not args.subject:
            print("❌ Please provide --subject for email")
            return
        
        if notifier.validate_email(args.email):
            notifier.send_email(args.email, args.subject, message, content_type)
        else:
            print(f"❌ Invalid email format: {args.email}")
    
    if args.sms:
        if not message:
            print("❌ Please provide --message")
            return
        
        if notifier.validate_phone(args.sms):
            notifier.send_sms(args.sms, message)
        else:
            print(f"❌ Invalid phone format: {args.sms}")
    
    # Send bulk notifications
    if args.bulk_email:
        if not message or not args.subject:
            print("❌ Please provide --subject and --message")
            return
        
        recipients = notifier.load_contacts(args.bulk_email)
        if recipients:
            notifier.send_bulk_email(recipients, args.subject, message, content_type)
    
    if args.bulk_sms:
        if not message:
            print("❌ Please provide --message")
            return
        
        recipients = notifier.load_contacts(args.bulk_sms)
        if recipients:
            notifier.send_bulk_sms(recipients, message)
    
    if not any([args.email, args.sms, args.bulk_email, args.bulk_sms, args.test, args.create_template]):
        print("❌ Please specify an action")
        print("Use --help for more information")


if __name__ == "__main__":
    main()