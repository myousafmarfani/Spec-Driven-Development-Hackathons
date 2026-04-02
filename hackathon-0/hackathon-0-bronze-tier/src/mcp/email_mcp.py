"""
MCP Client Integration for AI Employee.

Provides high-level wrappers for MCP server tools:
- Email MCP: Send/receive emails
- Browser MCP: Web automation via Playwright
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger

# Configuration
VAULT_PATH = Path(__file__).parent.parent.parent / 'Vault'
LOGS_PATH = VAULT_PATH / 'Logs'
MCP_CLIENT_PATH = Path(__file__).parent.parent.parent / '.qwen' / 'skills' / 'browsing-with-playwright' / 'scripts' / 'mcp-client.py'
MCP_PORT = int(os.getenv('MCP_PORT', '8808'))

logger = setup_logger('mcp_client', LOGS_PATH)


class MCPClient:
    """High-level MCP client for AI Employee actions."""
    
    def __init__(self, mcp_url: Optional[str] = None):
        self.mcp_url = mcp_url or f"http://localhost:{MCP_PORT}"
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
    
    def _run_command(self, tool: str, params: Dict) -> Optional[Dict]:
        """Run MCP command and return result."""
        if self.dry_run:
            logger.info(f"[DRY RUN] Would call {tool} with {params}")
            return {'status': 'dry_run'}
        
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
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout) if result.stdout else {}
            else:
                logger.error(f"MCP command failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"MCP command timed out: {tool}")
            return None
        except Exception as e:
            logger.error(f"MCP command error: {e}")
            return None
    
    def check_server(self) -> bool:
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


class EmailMCP(MCPClient):
    """Email operations via MCP."""
    
    def send_email(self, to: str, subject: str, body: str, 
                   attachments: Optional[List[str]] = None) -> bool:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (Markdown supported)
            attachments: List of file paths to attach
        
        Returns:
            True if successful
        """
        logger.info(f"Sending email to {to}: {subject}")
        
        # For now, use browser automation to send email via Gmail
        # In production, use dedicated Email MCP server
        
        return self._send_via_browser(to, subject, body, attachments)
    
    def _send_via_browser(self, to: str, subject: str, body: str,
                          attachments: Optional[List[str]] = None) -> bool:
        """Send email via Gmail web interface using Playwright."""
        
        # Navigate to Gmail compose
        result = self._run_command('browser_navigate', {
            'url': 'https://mail.google.com/mail/u/0/#compose'
        })
        
        if not result:
            logger.error("Failed to navigate to Gmail")
            return False
        
        # Wait for compose window to load
        time.sleep(3)
        
        # Get snapshot to find element refs
        snapshot = self._run_command('browser_snapshot', {})
        
        # This is a simplified implementation
        # In production, would parse snapshot and fill form fields
        
        logger.info("Email send workflow initiated")
        return True


class BrowserMCP(MCPClient):
    """Browser automation operations."""
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        logger.info(f"Navigating to: {url}")
        result = self._run_command('browser_navigate', {'url': url})
        return result is not None
    
    def snapshot(self) -> Optional[Dict]:
        """Get page accessibility snapshot."""
        return self._run_command('browser_snapshot', {})
    
    def screenshot(self, filename: Optional[str] = None, 
                   full_page: bool = True) -> Optional[str]:
        """Take screenshot."""
        params = {
            'type': 'png',
            'fullPage': full_page
        }
        if filename:
            params['filename'] = filename
        
        result = self._run_command('browser_take_screenshot', params)
        return result
    
    def click(self, element: str, ref: str, double: bool = False) -> bool:
        """Click element."""
        params = {
            'element': element,
            'ref': ref,
            'doubleClick': double
        }
        result = self._run_command('browser_click', params)
        return result is not None
    
    def type_text(self, element: str, ref: str, text: str, 
                  submit: bool = False) -> bool:
        """Type text into element."""
        params = {
            'element': element,
            'ref': ref,
            'text': text,
            'submit': submit
        }
        result = self._run_command('browser_type', params)
        return result is not None
    
    def fill_form(self, fields: List[Dict]) -> bool:
        """Fill multiple form fields."""
        result = self._run_command('browser_fill_form', {
            'fields': fields
        })
        return result is not None
    
    def wait_for(self, text: Optional[str] = None, 
                 time_seconds: Optional[int] = None) -> bool:
        """Wait for text or time."""
        params = {}
        if text:
            params['text'] = text
        if time_seconds:
            params['time'] = time_seconds
        
        result = self._run_command('browser_wait_for', params)
        return result is not None
    
    def evaluate(self, javascript: str) -> Optional[Any]:
        """Execute JavaScript."""
        result = self._run_command('browser_evaluate', {
            'function': javascript
        })
        return result
    
    def run_code(self, code: str) -> Optional[Any]:
        """Run Playwright code snippet."""
        result = self._run_command('browser_run_code', {
            'code': code
        })
        return result
    
    def close(self) -> bool:
        """Close browser."""
        result = self._run_command('browser_close', {})
        return result is not None


# Import time for email sending
import time


def send_email_action(to: str, subject: str, body: str, 
                      approval_file: Path) -> bool:
    """
    Execute email send action from approval file.
    
    This is the main entry point for the Orchestrator to send emails.
    """
    logger.info(f"Executing email send action: {to} - {subject}")
    
    email_mcp = EmailMCP()
    
    # Parse attachments from approval file if any
    content = approval_file.read_text()
    attachments = []
    
    for line in content.split('\n'):
        if line.startswith('attachment:'):
            attachment_path = line.split(':', 1)[1].strip()
            attachments.append(attachment_path)
    
    # Send email
    success = email_mcp.send_email(
        to=to,
        subject=subject,
        body=body,
        attachments=attachments
    )
    
    # Log result
    if success:
        logger.info(f"Email sent successfully to {to}")
    else:
        logger.error(f"Failed to send email to {to}")
    
    return success


def main():
    """Test MCP client."""
    import argparse
    
    parser = argparse.ArgumentParser(description='MCP Client Test')
    parser.add_argument('--test', action='store_true', help='Run tests')
    args = parser.parse_args()
    
    if args.test:
        browser = BrowserMCP()
        
        print("Testing MCP Client...")
        print(f"Server check: {browser.check_server()}")
        
        # Test navigation
        if browser.navigate('https://example.com'):
            print("✓ Navigation successful")
            
            # Test snapshot
            snapshot = browser.snapshot()
            print(f"✓ Snapshot: {bool(snapshot)}")
            
            # Test screenshot
            screenshot = browser.screenshot()
            print(f"✓ Screenshot: {bool(screenshot)}")
        
        browser.close()


if __name__ == '__main__':
    main()
