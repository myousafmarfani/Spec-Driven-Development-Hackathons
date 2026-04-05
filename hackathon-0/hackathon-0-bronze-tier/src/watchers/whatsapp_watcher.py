"""
WhatsApp Watcher - Monitors WhatsApp Web for new messages.

This watcher uses Playwright MCP to monitor WhatsApp Web and detect
messages that require action (invoice requests, meeting requests, etc.).

Note: Requires WhatsApp Web authentication and browser MCP server running.
"""

import os
import sys
import time
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger

# Configuration
VAULT_PATH = Path(__file__).parent.parent.parent / 'Vault'
NEEDS_ACTION_PATH = VAULT_PATH / 'Needs_Action'
LOGS_PATH = VAULT_PATH / 'Logs'
MCP_CLIENT_PATH = Path(__file__).parent.parent.parent / '.qwen' / 'skills' / 'browsing-with-playwright' / 'scripts' / 'mcp-client.py'
MCP_PORT = int(os.getenv('MCP_PORT', '8808'))

# Polling interval (seconds)
POLL_INTERVAL = int(os.getenv('WHATSAPP_POLL_INTERVAL', '30'))

# Trigger keywords
TRIGGER_KEYWORDS = ['invoice', 'payment', 'meeting', 'quote', 'proposal', 'urgent', 'asap']

logger = setup_logger('whatsapp_watcher', LOGS_PATH)


class WhatsAppWatcher:
    """Watch WhatsApp Web for new messages using Playwright MCP."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.mcp_url = f"http://localhost:{MCP_PORT}"
        self.seen_messages: set = set()
        self.last_check: Optional[datetime] = None
        self.browser_initialized = False
        
    def _run_mcp_command(self, tool: str, params: Dict) -> Optional[Dict]:
        """Run MCP command and return result."""
        try:
            cmd = [
                sys.executable,
                str(MCP_CLIENT_PATH),
                'call',
                '-u', self.mcp_url,
                '-t', tool,
                '-p', json.dumps(params)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout else None
            else:
                logger.error(f"MCP command failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"MCP command timed out: {tool}")
            return None
        except Exception as e:
            logger.error(f"MCP command error: {e}")
            return None
    
    def navigate_to_whatsapp(self) -> bool:
        """Navigate to WhatsApp Web."""
        logger.info("Navigating to WhatsApp Web...")
        
        result = self._run_mcp_command('browser_navigate', {
            'url': 'https://web.whatsapp.com'
        })
        
        if result:
            logger.info("Navigated to WhatsApp Web")
            # Wait for page to load
            time.sleep(5)
            return True
        
        logger.error("Failed to navigate to WhatsApp Web")
        return False
    
    def get_page_snapshot(self) -> Optional[Dict]:
        """Get accessibility snapshot of current page."""
        return self._run_mcp_command('browser_snapshot', {})
    
    def extract_messages(self, snapshot: Dict) -> List[Dict]:
        """Extract messages from page snapshot."""
        messages = []
        
        # Parse snapshot to find message elements
        # This is a simplified implementation - in production, use proper selectors
        content = str(snapshot)
        
        # Look for message patterns in the snapshot
        # Note: Actual implementation depends on WhatsApp Web structure
        lines = content.split('\n')
        
        for line in lines:
            # Simple heuristic: look for lines that might be messages
            if any(keyword in line.lower() for keyword in ['chat', 'message', 'text']):
                messages.append({
                    'text': line,
                    'timestamp': datetime.now().isoformat(),
                    'sender': 'unknown'
                })
        
        return messages
    
    def _check_triggers(self, message_text: str) -> List[str]:
        """Check if message matches any triggers."""
        triggers = []
        text_lower = message_text.lower()
        
        for keyword in TRIGGER_KEYWORDS:
            if keyword in text_lower:
                triggers.append(f"keyword:{keyword}")
        
        return triggers
    
    def _create_action_file(self, message: Dict, triggers: List[str]) -> Path:
        """Create action file in Needs_Action folder."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sender = message.get('sender', 'unknown').replace(' ', '_')
        filename = f"WHATSAPP_{sender}_{timestamp}.md"
        
        filepath = NEEDS_ACTION_PATH / filename
        
        content = f"""---
created: {datetime.now().isoformat()}
source: whatsapp
sender: {message.get('sender', 'unknown')}
text: {message.get('text', '')[:100]}
triggers: {', '.join(triggers)}
status: pending
---

# WhatsApp Message Received

**From:** {message.get('sender', 'Unknown')}  
**Time:** {message.get('timestamp', 'Unknown')}

## Message Content

{message.get('text', '')}

## Detected Triggers

{', '.join(triggers) if triggers else 'None'}

## Suggested Actions

<!-- Qwen Code will populate this -->

## Processing Log

- [{datetime.now().isoformat()}] Detected by WhatsApp Watcher
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
        try:
            # Get snapshot
            snapshot = self.get_page_snapshot()
            if not snapshot:
                logger.debug("No snapshot available")
                return 0
            
            # Extract messages
            messages = self.extract_messages(snapshot)
            
            if not messages:
                logger.debug("No new messages")
                return 0
            
            processed = 0
            for msg in messages:
                msg_id = hashlib.md5(msg['text'].encode()).hexdigest()
                
                # Skip already seen
                if msg_id in self.seen_messages:
                    continue
                
                # Check triggers
                triggers = self._check_triggers(msg['text'])
                
                if triggers:
                    # Create action file
                    self._create_action_file(msg, triggers)
                    processed += 1
                
                # Mark as seen
                self.seen_messages.add(msg_id)
            
            self.last_check = datetime.now()
            return processed
            
        except Exception as e:
            logger.error(f"Error checking messages: {e}")
            return 0
    
    def run(self):
        """Main watcher loop."""
        logger.info("Starting WhatsApp Watcher...")
        
        # Check MCP server
        if not self._check_mcp_server():
            logger.error("MCP server not running. Start with: bash scripts/start-server.sh")
            return
        
        # Navigate to WhatsApp
        if not self.navigate_to_whatsapp():
            logger.error("Failed to load WhatsApp Web. Waiting for manual login...")
            # Give user time to log in
            time.sleep(30)
        
        logger.info(f"Polling every {POLL_INTERVAL} seconds")
        logger.info(f"Triggers: {TRIGGER_KEYWORDS}")
        
        try:
            while True:
                processed = self.check_for_new_messages()
                if processed > 0:
                    logger.info(f"Processed {processed} messages")
                
                time.sleep(POLL_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("WhatsApp Watcher stopped by user")
        except Exception as e:
            logger.error(f"Watcher crashed: {e}")
            raise
    
    def _check_mcp_server(self) -> bool:
        """Check if MCP server is running."""
        try:
            result = subprocess.run(
                ['pgrep', '-f', '@playwright/mcp'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            # Windows fallback
            return True


def main():
    """Entry point."""
    import argparse
    import hashlib
    
    parser = argparse.ArgumentParser(description='WhatsApp Watcher')
    parser.add_argument('--dry-run', action='store_true', help='Run without creating files')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    args = parser.parse_args()
    
    watcher = WhatsAppWatcher(dry_run=args.dry_run)
    
    if args.once:
        # Run once for testing
        processed = watcher.check_for_new_messages()
        print(f"Processed {processed} messages")
        sys.exit(0 if processed >= 0 else 1)
    else:
        watcher.run()


if __name__ == '__main__':
    main()
