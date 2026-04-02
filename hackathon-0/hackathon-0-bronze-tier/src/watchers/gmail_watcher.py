"""
Gmail Watcher - Monitors Gmail for new messages matching triggers.

This watcher continuously polls Gmail API for new messages and creates
action files in /Vault/Needs_Action/ when triggers are detected.

Triggers:
- Keywords: "invoice", "payment", "meeting", "urgent", "asap"
- Unknown senders (for approval)
- VIP senders (for priority handling)
"""

import os
import sys
import time
import json
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger

# Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = Path(__file__).parent.parent.parent / 'credentials' / 'gmail_token.json'
CREDENTIALS_PATH = Path(__file__).parent.parent.parent / 'credentials' / 'credentials.json'
VAULT_PATH = Path(__file__).parent.parent.parent / 'Vault'
NEEDS_ACTION_PATH = VAULT_PATH / 'Needs_Action'
LOGS_PATH = VAULT_PATH / 'Logs'

# Polling interval (seconds)
POLL_INTERVAL = int(os.getenv('GMAIL_POLL_INTERVAL', '60'))

# Trigger keywords
TRIGGER_KEYWORDS = ['invoice', 'payment', 'meeting', 'urgent', 'asap', 'quote', 'proposal']

logger = setup_logger('gmail_watcher', LOGS_PATH)


class GmailWatcher:
    """Watch Gmail for new messages and create action files."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.service: Optional[Any] = None
        self.seen_message_ids: set = set()
        self.last_check: Optional[datetime] = None
        
        # Load VIP contacts
        self.vip_contacts = self._load_vip_contacts()
        
    def _load_vip_contacts(self) -> set:
        """Load VIP contacts from Company Handbook."""
        handbook_path = VAULT_PATH / 'Company_Handbook.md'
        vip_contacts = set()
        
        if handbook_path.exists():
            content = handbook_path.read_text()
            # Simple parsing - in production, use proper Markdown parser
            in_vip_section = False
            for line in content.split('\n'):
                if 'VIP Contacts' in line:
                    in_vip_section = True
                elif in_vip_section and line.startswith('###'):
                    in_vip_section = False
                elif in_vip_section and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        email = parts[2].strip()
                        if '@' in email:
                            vip_contacts.add(email.lower())
        
        return vip_contacts
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        creds = None
        
        # Load existing token
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Token refresh failed: {e}")
                    return False
            else:
                if not CREDENTIALS_PATH.exists():
                    logger.error(f"Credentials file not found: {CREDENTIALS_PATH}")
                    logger.error("Please download credentials from Google Cloud Console")
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_PATH, SCOPES
                    )
                    creds = flow.run_local_server(port=8080, open_browser=False)
                    
                    # Save credentials
                    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
                    with open(TOKEN_PATH, 'w') as token:
                        token.write(creds.to_json())
                    
                    logger.info("Gmail authentication successful")
                except Exception as e:
                    logger.error(f"Authentication failed: {e}")
                    return False
        
        # Build service
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            return True
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            return False
    
    def _get_message(self, msg_id: str) -> Optional[Dict]:
        """Get full message by ID."""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            return message
        except HttpError as e:
            logger.error(f"Error getting message {msg_id}: {e}")
            return None
    
    def _extract_email_info(self, message: Dict) -> Dict:
        """Extract relevant info from Gmail message."""
        headers = message.get('payload', {}).get('headers', [])
        
        email_info = {
            'id': message['id'],
            'subject': '',
            'from': '',
            'to': '',
            'date': '',
            'snippet': message.get('snippet', ''),
            'body': ''
        }
        
        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            
            if name == 'subject':
                email_info['subject'] = value
            elif name == 'from':
                email_info['from'] = value
            elif name == 'to':
                email_info['to'] = value
            elif name == 'date':
                email_info['date'] = value
        
        # Extract body
        body = self._extract_body(message)
        email_info['body'] = body
        
        return email_info
    
    def _extract_body(self, message: Dict) -> str:
        """Extract email body from message parts."""
        def get_text_from_parts(parts):
            text = ""
            if parts:
                for part in parts:
                    mime_type = part.get('mimeType', '')
                    if mime_type == 'text/plain':
                        data = part.get('body', {}).get('data', '')
                        if data:
                            import base64
                            text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    elif part.get('parts'):
                        text += get_text_from_parts(part['parts'])
            return text
        
        return get_text_from_parts(message.get('payload', {}).get('parts', []))
    
    def _check_triggers(self, email_info: Dict) -> List[str]:
        """Check if email matches any triggers."""
        triggers = []
        
        subject = email_info['subject'].lower()
        body = email_info['body'].lower()
        text = f"{subject} {body}"
        
        # Check for trigger keywords
        for keyword in TRIGGER_KEYWORDS:
            if keyword in text:
                triggers.append(f"keyword:{keyword}")
        
        # Check if from VIP
        from_email = email_info['from'].lower()
        for vip in self.vip_contacts:
            if vip in from_email:
                triggers.append("vip_sender")
                break
        
        return triggers
    
    def _create_action_file(self, email_info: Dict, triggers: List[str]) -> Path:
        """Create action file in Needs_Action folder."""
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        from_email = email_info['from'].replace(' ', '_').replace('<', '').replace('>', '')
        filename = f"GMAIL_{from_email}_{timestamp}.md"
        
        filepath = NEEDS_ACTION_PATH / filename
        
        # Create content
        content = f"""---
created: {datetime.now().isoformat()}
source: gmail
message_id: {email_info['id']}
from: {email_info['from']}
subject: {email_info['subject']}
date: {email_info['date']}
triggers: {', '.join(triggers)}
status: pending
---

# Email Received

**From:** {email_info['from']}  
**Subject:** {email_info['subject']}  
**Date:** {email_info['date']}

## Content

{email_info['snippet']}

{email_info['body']}

## Suggested Actions

<!-- Claude Code will populate this -->

## Processing Log

- [{datetime.now().isoformat()}] Detected by Gmail Watcher
- [{datetime.now().isoformat()}] Triggers: {', '.join(triggers)}
"""
        
        if not self.dry_run:
            filepath.write_text(content)
            logger.info(f"Created action file: {filepath}")
        else:
            logger.info(f"[DRY RUN] Would create: {filepath}")
        
        return filepath
    
    def check_for_new_messages(self) -> int:
        """Check for new messages and process triggers."""
        if not self.service:
            logger.error("Gmail service not initialized")
            return 0
        
        try:
            # Build query for unread messages from last check
            if self.last_check:
                query = f'is:unread after:{self.last_check.strftime("%Y/%m/%d")}'
            else:
                query = 'is:unread'
            
            # Fetch messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=10,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                logger.debug("No new messages")
                return 0
            
            processed = 0
            for msg in messages:
                msg_id = msg['id']
                
                # Skip already seen
                if msg_id in self.seen_message_ids:
                    continue
                
                # Get full message
                message = self._get_message(msg_id)
                if not message:
                    continue
                
                # Extract info
                email_info = self._extract_email_info(message)
                
                # Check triggers
                triggers = self._check_triggers(email_info)
                
                if triggers:
                    # Create action file
                    self._create_action_file(email_info, triggers)
                    processed += 1
                
                # Mark as seen
                self.seen_message_ids.add(msg_id)
            
            self.last_check = datetime.now()
            return processed
            
        except HttpError as e:
            logger.error(f"Gmail API error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return 0
    
    def run(self):
        """Main watcher loop."""
        logger.info("Starting Gmail Watcher...")
        
        # Authenticate
        if not self.authenticate():
            logger.error("Authentication failed. Exiting.")
            return
        
        logger.info(f"Polling every {POLL_INTERVAL} seconds")
        logger.info(f"Triggers: {TRIGGER_KEYWORDS}")
        logger.info(f"VIP contacts: {len(self.vip_contacts)}")
        
        try:
            while True:
                processed = self.check_for_new_messages()
                if processed > 0:
                    logger.info(f"Processed {processed} messages")
                
                time.sleep(POLL_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Gmail Watcher stopped by user")
        except Exception as e:
            logger.error(f"Watcher crashed: {e}")
            raise


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail Watcher')
    parser.add_argument('--dry-run', action='store_true', help='Run without creating files')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()
    
    watcher = GmailWatcher(dry_run=args.dry_run)
    
    if args.once:
        # Run once for testing
        if watcher.authenticate():
            processed = watcher.check_for_new_messages()
            print(f"Processed {processed} messages")
            sys.exit(0 if processed >= 0 else 1)
        else:
            sys.exit(1)
    else:
        watcher.run()


if __name__ == '__main__':
    main()
