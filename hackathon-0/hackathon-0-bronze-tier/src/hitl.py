"""
Human-in-the-Loop (HITL) System for AI Employee.

Provides approval workflow management:
- Create approval requests
- Track approval status
- Enforce approval thresholds
- Audit trail maintenance
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger, log_action

# Configuration
VAULT_PATH = Path(__file__).parent.parent.parent / 'Vault'
PENDING_APPROVAL_PATH = VAULT_PATH / 'Pending_Approval'
APPROVED_PATH = VAULT_PATH / 'Approved'
REJECTED_PATH = VAULT_PATH / 'Rejected'
LOGS_PATH = VAULT_PATH / 'Logs'

logger = setup_logger('hitl', LOGS_PATH)


# Approval thresholds from Company Handbook
APPROVAL_THRESHOLDS = {
    'email': {
        'auto_approve_known_contacts': True,
        'require_approval_new_contacts': True,
        'require_approval_bulk': True,  # > 5 recipients
    },
    'payment': {
        'auto_approve_recurring_under': 50,  # USD
        'require_approval_new_payee': True,
        'require_approval_over': 100,  # USD
    },
    'social_media': {
        'auto_approve_scheduled': True,
        'require_approval_replies': True,
        'require_approval_dm': True,
    },
    'file_operations': {
        'auto_approve_create': True,
        'auto_approve_read': True,
        'auto_approve_move_internal': True,  # Within Vault
        'require_approval_delete': True,
        'require_approval_move_external': True,
    }
}


class ApprovalRequest:
    """Represents an approval request."""
    
    def __init__(self, action_type: str, description: str, 
                 details: Dict, priority: str = 'normal'):
        self.id = f"{action_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.action_type = action_type
        self.description = description
        self.details = details
        self.priority = priority
        self.created_at = datetime.now()
        self.status = 'pending'  # pending, approved, rejected
        self.approved_by: Optional[str] = None
        self.approved_at: Optional[datetime] = None
        self.rejected_by: Optional[str] = None
        self.rejected_at: Optional[datetime] = None
        self.reason: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'action_type': self.action_type,
            'description': self.description,
            'details': self.details,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejected_by': self.rejected_by,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'reason': self.reason
        }
    
    def to_markdown(self) -> str:
        """Convert to Markdown file content."""
        return f"""---
id: {self.id}
created: {self.created_at.isoformat()}
action_type: {self.action_type}
status: {self.status}
priority: {self.priority}
---

# Approval Request

**ID:** {self.id}  
**Type:** {self.action_type}  
**Priority:** {self.priority}  
**Created:** {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}

## Description

{self.description}

## Details

{json.dumps(self.details, indent=2)}

## Instructions

1. Review the details above
2. To approve: Move this file to `/Approved/`
3. To reject: Move this file to `/Rejected/`

## Processing Log

- [{self.created_at.isoformat()}] Request created
"""


class HITLManager:
    """Manage Human-in-the-Loop approvals."""
    
    def __init__(self):
        self.thresholds = APPROVAL_THRESHOLDS
        
        # Ensure directories exist
        for path in [PENDING_APPROVAL_PATH, APPROVED_PATH, REJECTED_PATH]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _get_pending_requests(self) -> List[Path]:
        """Get all pending approval requests."""
        if not PENDING_APPROVAL_PATH.exists():
            return []
        
        return sorted(
            PENDING_APPROVAL_PATH.glob('*.md'),
            key=lambda x: x.stat().st_mtime
        )
    
    def create_request(self, action_type: str, description: str,
                       details: Dict, priority: str = 'normal') -> ApprovalRequest:
        """
        Create a new approval request.
        
        Args:
            action_type: Type of action (email_send, payment, etc.)
            description: Human-readable description
            details: Action-specific details
            priority: 'low', 'normal', 'high', 'urgent'
        
        Returns:
            ApprovalRequest object
        """
        request = ApprovalRequest(
            action_type=action_type,
            description=description,
            details=details,
            priority=priority
        )
        
        # Save to Pending_Approval folder
        filename = f"{request.id}.md"
        filepath = PENDING_APPROVAL_PATH / filename
        
        filepath.write_text(request.to_markdown())
        
        logger.info(f"Created approval request: {request.id}")
        log_action(
            LOGS_PATH,
            'approval_request_created',
            request_id=request.id,
            action_type=action_type,
            priority=priority
        )
        
        return request
    
    def approve_request(self, request_id: str, approved_by: str = 'human') -> bool:
        """
        Approve a request.
        
        In production, this is triggered by moving file to /Approved/
        """
        # Find request file
        filepath = PENDING_APPROVAL_PATH / f"{request_id}.md"
        
        if not filepath.exists():
            # Check if already processed
            filepath = APPROVED_PATH / f"{request_id}.md"
            if filepath.exists():
                logger.info(f"Request {request_id} already approved")
                return True
            logger.error(f"Request not found: {request_id}")
            return False
        
        # Read and update
        content = filepath.read_text()
        
        # Update status
        content = content.replace(
            'status: pending',
            f'status: approved\napproved_by: {approved_by}\napproved_at: {datetime.now().isoformat()}'
        )
        
        # Move to Approved
        dest = APPROVED_PATH / f"{request_id}.md"
        dest.write_text(content)
        filepath.unlink()
        
        logger.info(f"Approved request: {request_id}")
        log_action(
            LOGS_PATH,
            'approval_request_approved',
            request_id=request_id,
            approved_by=approved_by
        )
        
        return True
    
    def reject_request(self, request_id: str, rejected_by: str = 'human',
                       reason: Optional[str] = None) -> bool:
        """
        Reject a request.
        
        In production, this is triggered by moving file to /Rejected/
        """
        # Find request file
        filepath = PENDING_APPROVAL_PATH / f"{request_id}.md"
        
        if not filepath.exists():
            logger.error(f"Request not found: {request_id}")
            return False
        
        # Read and update
        content = filepath.read_text()
        
        # Update status
        content = content.replace(
            'status: pending',
            f'status: rejected\nrejected_by: {rejected_by}\nrejected_at: {datetime.now().isoformat()}\nreason: {reason or "No reason provided"}'
        )
        
        # Move to Rejected
        dest = REJECTED_PATH / f"{request_id}.md"
        dest.write_text(content)
        filepath.unlink()
        
        logger.info(f"Rejected request: {request_id}")
        log_action(
            LOGS_PATH,
            'approval_request_rejected',
            request_id=request_id,
            rejected_by=rejected_by,
            reason=reason
        )
        
        return True
    
    def check_auto_approve(self, action_type: str, details: Dict) -> bool:
        """
        Check if action qualifies for auto-approval.
        
        Args:
            action_type: Type of action
            details: Action details
        
        Returns:
            True if auto-approved
        """
        if action_type not in self.thresholds:
            return False
        
        thresholds = self.thresholds[action_type]
        
        if action_type == 'email':
            return self._check_email_auto_approve(details, thresholds)
        elif action_type == 'payment':
            return self._check_payment_auto_approve(details, thresholds)
        elif action_type == 'social_media':
            return self._check_social_auto_approve(details, thresholds)
        elif action_type == 'file_operations':
            return self._check_file_auto_approve(details, thresholds)
        
        return False
    
    def _check_email_auto_approve(self, details: Dict, thresholds: Dict) -> bool:
        """Check email auto-approval conditions."""
        # Check if sending to known contact
        to = details.get('to', '')
        known_contacts = self._load_known_contacts()
        
        if to.lower() not in known_contacts:
            return False
        
        # Check if bulk email
        recipients = details.get('recipients', [to])
        if len(recipients) > 5:
            return False
        
        return thresholds.get('auto_approve_known_contacts', False)
    
    def _check_payment_auto_approve(self, details: Dict, thresholds: Dict) -> bool:
        """Check payment auto-approval conditions."""
        amount = float(details.get('amount', 0))
        payee = details.get('payee', '')
        is_recurring = details.get('recurring', False)
        
        # New payee always requires approval
        known_payees = self._load_known_payees()
        if payee not in known_payees:
            return False
        
        # Check amount thresholds
        if amount >= thresholds.get('require_approval_over', 100):
            return False
        
        # Recurring payments under threshold
        if is_recurring and amount < thresholds.get('auto_approve_recurring_under', 50):
            return True
        
        return False
    
    def _check_social_auto_approve(self, details: Dict, thresholds: Dict) -> bool:
        """Check social media auto-approval conditions."""
        action = details.get('action', '')
        
        if action == 'scheduled_post':
            return thresholds.get('auto_approve_scheduled', False)
        elif action in ['reply', 'dm']:
            return False
        
        return False
    
    def _check_file_auto_approve(self, details: Dict, thresholds: Dict) -> bool:
        """Check file operation auto-approval conditions."""
        operation = details.get('operation', '')
        
        if operation == 'create':
            return thresholds.get('auto_approve_create', False)
        elif operation == 'read':
            return thresholds.get('auto_approve_read', False)
        elif operation == 'delete':
            return False
        elif operation == 'move':
            source = details.get('source', '')
            dest = details.get('dest', '')
            
            # Moving within Vault is auto-approved
            if 'Vault/' in source and 'Vault/' in dest:
                return thresholds.get('auto_approve_move_internal', False)
            
            return False
        
        return False
    
    def _load_known_contacts(self) -> set:
        """Load known contacts from vault."""
        contacts_file = VAULT_PATH / 'Contacts.md'
        contacts = set()
        
        if contacts_file.exists():
            content = contacts_file.read_text()
            for line in content.split('\n'):
                if '@' in line:
                    # Extract email from line
                    parts = line.split('|')
                    for part in parts:
                        if '@' in part:
                            contacts.add(part.strip().lower())
        
        return contacts
    
    def _load_known_payees(self) -> set:
        """Load known payees from vault."""
        # Similar to contacts, would load from Accounting folder
        return set()
    
    def get_pending_count(self) -> int:
        """Get count of pending approvals."""
        return len(self._get_pending_requests())
    
    def get_pending_list(self) -> List[Dict]:
        """Get list of pending approvals."""
        requests = []
        
        for filepath in self._get_pending_requests():
            content = filepath.read_text()
            
            # Parse frontmatter
            request_info = {
                'filename': filepath.name,
                'path': str(filepath)
            }
            
            for line in content.split('\n'):
                if line.startswith('action_type:'):
                    request_info['action_type'] = line.split(':', 1)[1].strip()
                elif line.startswith('priority:'):
                    request_info['priority'] = line.split(':', 1)[1].strip()
                elif line.startswith('created:'):
                    request_info['created'] = line.split(':', 1)[1].strip()
            
            requests.append(request_info)
        
        return requests


# Global instance
hitl_manager = HITLManager()


def create_approval_request(action_type: str, description: str,
                            details: Dict, priority: str = 'normal') -> ApprovalRequest:
    """Create an approval request."""
    return hitl_manager.create_request(action_type, description, details, priority)


def check_auto_approve(action_type: str, details: Dict) -> bool:
    """Check if action qualifies for auto-approval."""
    return hitl_manager.check_auto_approve(action_type, details)


def main():
    """Test HITL system."""
    manager = HITLManager()
    
    print("HITL Manager Test")
    print("=" * 40)
    
    # Create test request
    request = manager.create_request(
        action_type='email_send',
        description='Send invoice to client',
        details={
            'to': 'client@example.com',
            'subject': 'Invoice #123',
            'amount': 1500
        },
        priority='normal'
    )
    
    print(f"Created request: {request.id}")
    print(f"Pending count: {manager.get_pending_count()}")
    print(f"Pending list: {manager.get_pending_list()}")


if __name__ == '__main__':
    main()
