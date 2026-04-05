"""
Orchestrator - Master process for the AI Employee system.

The Orchestrator:
1. Monitors Needs_Action folder for new tasks
2. Invokes Qwen Code to analyze and create plans
3. Manages Human-in-the-Loop approval workflow
4. Executes approved actions via MCP servers
5. Updates Dashboard with activity
"""

import os
import sys
import time
import json
import logging
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger, log_action

# Configuration
VAULT_PATH = Path(__file__).parent.parent / 'Vault'
NEEDS_ACTION_PATH = VAULT_PATH / 'Needs_Action'
PLANS_PATH = VAULT_PATH / 'Plans'
PENDING_APPROVAL_PATH = VAULT_PATH / 'Pending_Approval'
APPROVED_PATH = VAULT_PATH / 'Approved'
REJECTED_PATH = VAULT_PATH / 'Rejected'
DONE_PATH = VAULT_PATH / 'Done'
LOGS_PATH = VAULT_PATH / 'Logs'
DASHBOARD_PATH = VAULT_PATH / 'Dashboard.md'

# Orchestrator settings
CHECK_INTERVAL = int(os.getenv('ORCHESTRATOR_CHECK_INTERVAL', '30'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

logger = setup_logger('orchestrator', LOGS_PATH)


class Orchestrator:
    """Main orchestrator for AI Employee system."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.processing_files: set = set()
        self.qwen_available = self._check_qwen_code()
        
        # Ensure all directories exist
        for path in [NEEDS_ACTION_PATH, PLANS_PATH, PENDING_APPROVAL_PATH, 
                     APPROVED_PATH, REJECTED_PATH, DONE_PATH, LOGS_PATH]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _check_qwen_code(self) -> bool:
        """Check if Qwen Code is available."""
        try:
            result = subprocess.run(
                ['qwen', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Qwen Code available: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"Qwen Code not available: {e}")
            logger.warning("Install Qwen Code to enable AI reasoning")
        return False
    
    def _get_pending_files(self) -> List[Path]:
        """Get files in Needs_Action folder."""
        if not NEEDS_ACTION_PATH.exists():
            return []
        
        files = []
        for f in NEEDS_ACTION_PATH.glob('*.md'):
            if f not in self.processing_files:
                files.append(f)
        
        return sorted(files, key=lambda x: x.stat().st_mtime)
    
    def _get_approved_files(self) -> List[Path]:
        """Get files in Approved folder ready for execution."""
        if not APPROVED_PATH.exists():
            return []
        
        files = []
        for f in APPROVED_PATH.glob('*.md'):
            # Check if already processed
            if not self._is_processed(f):
                files.append(f)
        
        return files
    
    def _is_processed(self, filepath: Path) -> bool:
        """Check if file has been processed."""
        content = filepath.read_text()
        return 'processed_at:' in content
    
    def _invoke_qwen(self, input_file: Path) -> Optional[Path]:
        """
        Invoke Qwen Code to analyze input and create plan.

        Returns path to plan file if successful.
        """
        logger.info(f"Invoking Qwen Code for: {input_file.name}")

        # Create plan file path
        plan_filename = f"PLAN_{input_file.stem}.md"
        plan_path = PLANS_PATH / plan_filename

        if self.dry_run:
            logger.info(f"[DRY RUN] Would invoke Qwen Code for: {input_file.name}")
            return None

        if not self.qwen_available:
            logger.error("Qwen Code not available")
            return None

        # Build Qwen Code command
        # This uses Qwen Code CLI to analyze the file and create a plan
        prompt = f"""
Analyze this action file and create a detailed plan:

1. Identify the objective
2. List required steps
3. Identify any approvals needed
4. Create a structured plan file

Action file content:
{input_file.read_text()}

Create a plan file at: {plan_path}

Format the plan as:
---
created: [timestamp]
status: pending_approval
objective: [clear objective]
---

## Objective
[Clear statement]

## Steps
- [ ] Step 1
- [ ] Step 2

## Approval Required
[List any actions requiring human approval]
"""

        try:
            result = subprocess.run(
                ['qwen', '--prompt', prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f"Qwen Code completed analysis")

                # If Qwen didn't create the file, create a basic plan
                if not plan_path.exists():
                    self._create_basic_plan(input_file, plan_path)

                return plan_path
            else:
                logger.error(f"Qwen Code error: {result.stderr}")
                self._create_basic_plan(input_file, plan_path)
                return plan_path

        except subprocess.TimeoutExpired:
            logger.error("Qwen Code timed out")
            self._create_basic_plan(input_file, plan_path)
            return plan_path
        except Exception as e:
            logger.error(f"Error invoking Qwen Code: {e}")
            self._create_basic_plan(input_file, plan_path)
            return plan_path
    
    def _create_basic_plan(self, input_file: Path, plan_path: Path):
        """Create a basic plan if Qwen is unavailable."""
        content = input_file.read_text()
        
        # Extract metadata from frontmatter
        source = 'unknown'
        for line in content.split('\n'):
            if line.startswith('source:'):
                source = line.split(':')[1].strip()
                break
        
        plan_content = f"""---
created: {datetime.now().isoformat()}
status: pending_approval
source: {source}
input_file: {str(input_file)}
---

# Action Plan

## Objective
Process action from {source}

## Steps
- [ ] Review input file
- [ ] Determine required actions
- [ ] Request human approval if needed
- [ ] Execute approved actions
- [ ] Log results

## Approval Required
Move this file to /Approved/ to proceed, or /Rejected/ to cancel.

## Input Reference
See: {input_file}
"""
        
        plan_path.write_text(plan_content)
        logger.info(f"Created basic plan: {plan_path}")
    
    def _create_approval_request(self, plan_file: Path) -> Path:
        """Create approval request file."""
        content = plan_file.read_text()
        
        # Extract objective
        objective = 'Action Required'
        for line in content.split('\n'):
            if line.startswith('objective:'):
                objective = line.split(':', 1)[1].strip()
                break
        
        approval_filename = f"APPROVAL_{plan_file.stem}.md"
        approval_path = PENDING_APPROVAL_PATH / approval_filename
        
        approval_content = f"""---
created: {datetime.now().isoformat()}
plan_file: {str(plan_file)}
objective: {objective}
status: pending
---

# Approval Required

**Objective:** {objective}

**Plan:** {plan_file.name}

## Instructions

1. Review the plan file above
2. If you approve, move this file to `/Approved/`
3. If you reject, move this file to `/Rejected/`

## Details

{content}
"""
        
        if not self.dry_run:
            approval_path.write_text(approval_content)
            logger.info(f"Created approval request: {approval_path}")
        else:
            logger.info(f"[DRY RUN] Would create approval request: {approval_path}")
        
        return approval_path
    
    def _execute_approved_action(self, approved_file: Path) -> bool:
        """
        Execute an approved action.
        
        Returns True if successful.
        """
        logger.info(f"Executing approved action: {approved_file.name}")
        
        content = approved_file.read_text()
        
        # Parse action type from content
        action_type = 'unknown'
        for line in content.split('\n'):
            if line.startswith('action_type:'):
                action_type = line.split(':', 1)[1].strip()
                break
            elif 'send_email' in line.lower():
                action_type = 'email_send'
                break
            elif 'payment' in line.lower():
                action_type = 'payment'
                break
        
        # Execute based on action type
        success = False
        
        if action_type == 'email_send':
            success = self._execute_email_send(approved_file)
        elif action_type == 'payment':
            success = self._execute_payment(approved_file)
        else:
            logger.info(f"Generic action execution: {action_type}")
            success = True  # Assume success for generic actions
        
        # Mark as processed
        if success:
            self._mark_processed(approved_file)
            log_action(
                LOGS_PATH,
                action_type,
                file=str(approved_file),
                result='success'
            )
        else:
            log_action(
                LOGS_PATH,
                action_type,
                file=str(approved_file),
                result='failure'
            )
        
        return success
    
    def _execute_email_send(self, approved_file: Path) -> bool:
        """Execute email send action."""
        logger.info("Executing email send...")
        
        if self.dry_run:
            logger.info("[DRY RUN] Would send email")
            return True
        
        # Parse email details from approved file
        content = approved_file.read_text()
        
        # In production, use MCP client to send email
        # For now, log the action
        logger.info(f"Email would be sent (details in {approved_file})")
        
        return True
    
    def _execute_payment(self, approved_file: Path) -> bool:
        """Execute payment action."""
        logger.info("Executing payment...")
        
        if self.dry_run:
            logger.info("[DRY RUN] Would process payment")
            return True
        
        # In production, use banking API or MCP
        logger.info(f"Payment would be processed (details in {approved_file})")
        
        return True
    
    def _mark_processed(self, filepath: Path):
        """Mark file as processed."""
        content = filepath.read_text()
        
        # Add processed timestamp
        if 'processed_at:' not in content:
            content += f"\n\n---\nprocessed_at: {datetime.now().isoformat()}\n"
            filepath.write_text(content)
    
    def _move_to_done(self, *files: Path):
        """Move files to Done folder."""
        for f in files:
            if f.exists():
                dest = DONE_PATH / f.name
                try:
                    shutil.move(str(f), str(dest))
                    logger.debug(f"Moved to Done: {f.name}")
                except Exception as e:
                    logger.error(f"Error moving {f.name}: {e}")
    
    def _update_dashboard(self):
        """Update the Dashboard.md with current status."""
        if not DASHBOARD_PATH.exists():
            return
        
        # Count files in each folder
        needs_action_count = len(list(NEEDS_ACTION_PATH.glob('*.md')))
        pending_count = len(list(PENDING_APPROVAL_PATH.glob('*.md')))
        approved_count = len(list(APPROVED_PATH.glob('*.md')))
        done_today = len([f for f in DONE_PATH.glob('*.md') 
                         if datetime.fromtimestamp(f.stat().st_mtime).date() == datetime.now().date()])
        
        # Get recent activity
        recent_files = sorted(DONE_PATH.glob('*.md'), 
                             key=lambda x: x.stat().st_mtime, 
                             reverse=True)[:5]
        
        activity_lines = []
        for f in recent_files:
            timestamp = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            activity_lines.append(f"- [{timestamp}] {f.name}")
        
        # Read current dashboard
        content = DASHBOARD_PATH.read_text()
        
        # Update placeholders
        replacements = {
            '{{TIMESTAMP}}': datetime.now().isoformat(),
            '{{STATUS}}': 'Running',
            '{{NEEDS_ACTION_COUNT}}': str(needs_action_count),
            '{{PENDING_COUNT}}': str(pending_count),
            '{{RECENT_ACTIVITY}}': '\n'.join(activity_lines) if activity_lines else '- No recent activity',
            '{{LAST_REFRESH}}': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for key, value in replacements.items():
            content = content.replace(key, value)
        
        if not self.dry_run:
            DASHBOARD_PATH.write_text(content)
            logger.debug("Dashboard updated")
    
    def process_needs_action(self):
        """Process files in Needs_Action folder."""
        files = self._get_pending_files()
        
        for input_file in files:
            logger.info(f"Processing: {input_file.name}")
            self.processing_files.add(input_file)
            
            try:
                # Invoke Qwen to create plan
                plan_file = self._invoke_qwen(input_file)
                
                if plan_file:
                    # Create approval request
                    self._create_approval_request(plan_file)
                    
                    # Move input to Done
                    self._move_to_done(input_file)
                    
            except Exception as e:
                logger.error(f"Error processing {input_file.name}: {e}")
            finally:
                self.processing_files.discard(input_file)
    
    def process_approved(self):
        """Process files in Approved folder."""
        files = self._get_approved_files()
        
        for approved_file in files:
            logger.info(f"Executing: {approved_file.name}")
            
            try:
                success = self._execute_approved_action(approved_file)
                
                if success:
                    self._move_to_done(approved_file)
                    
            except Exception as e:
                logger.error(f"Error executing {approved_file.name}: {e}")
    
    def run(self):
        """Main orchestrator loop."""
        logger.info("=" * 50)
        logger.info("AI Employee Orchestrator Starting...")
        logger.info(f"Vault: {VAULT_PATH}")
        logger.info(f"Dry Run: {self.dry_run}")
        logger.info(f"Qwen Code: {'Available' if self.qwen_available else 'Not Available'}")
        logger.info("=" * 50)
        
        try:
            while True:
                # Process new actions
                self.process_needs_action()
                
                # Execute approved actions
                self.process_approved()
                
                # Update dashboard
                self._update_dashboard()
                
                # Wait before next cycle
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")
        except Exception as e:
            logger.error(f"Orchestrator crashed: {e}")
            raise


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('--dry-run', action='store_true', help='Run without executing actions')
    parser.add_argument('--once', action='store_true', help='Run one cycle and exit')
    args = parser.parse_args()
    
    orchestrator = Orchestrator(dry_run=args.dry_run)
    
    if args.once:
        # Run one cycle for testing
        orchestrator.process_needs_action()
        orchestrator.process_approved()
        orchestrator._update_dashboard()
        sys.exit(0)
    else:
        orchestrator.run()


if __name__ == '__main__':
    main()
