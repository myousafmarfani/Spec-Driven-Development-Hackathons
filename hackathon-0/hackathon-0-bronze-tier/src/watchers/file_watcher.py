"""
File Watcher - Monitors filesystem for changes.

This watcher monitors specific folders for new or modified files
and triggers AI processing when changes are detected.

Monitored folders:
- /Vault/Incoming/ - New files to process
- /Vault/Approved/ - Files ready for action
"""

import os
import sys
import time
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger

# Configuration
VAULT_PATH = Path(__file__).parent.parent.parent / 'Vault'
INCOMING_PATH = VAULT_PATH / 'Incoming'
APPROVED_PATH = VAULT_PATH / 'Approved'
LOGS_PATH = VAULT_PATH / 'Logs'

logger = setup_logger('file_watcher', LOGS_PATH)


class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events."""
    
    def __init__(self, callback, dry_run: bool = False):
        self.callback = callback
        self.dry_run = dry_run
        self.file_hashes: Dict[Path, str] = {}
        
    def _get_file_hash(self, path: Path) -> str:
        """Calculate file hash."""
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error hashing {path}: {e}")
            return ""
    
    def _should_process(self, path: Path) -> bool:
        """Check if file should be processed."""
        # Only process Markdown files
        if not path.suffix.lower() in ['.md', '.markdown']:
            return False
        
        # Skip hidden files
        if path.name.startswith('.'):
            return False
        
        # Check if file is new or modified
        current_hash = self._get_file_hash(path)
        previous_hash = self.file_hashes.get(path, "")
        
        if current_hash and current_hash != previous_hash:
            self.file_hashes[path] = current_hash
            return True
        
        return False
    
    def on_created(self, event):
        """Handle file creation."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        logger.info(f"File created: {path}")
        
        if self._should_process(path):
            self.callback('created', path)
    
    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        logger.debug(f"File modified: {path}")
        
        if self._should_process(path):
            self.callback('modified', path)


class FileWatcher:
    """Watch filesystem for changes."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.observer: Optional[Observer] = None
        self.pending_files: List[Path] = []
        
        # Ensure directories exist
        INCOMING_PATH.mkdir(parents=True, exist_ok=True)
        APPROVED_PATH.mkdir(parents=True, exist_ok=True)
    
    def _process_file(self, event_type: str, path: Path):
        """Process a file change event."""
        logger.info(f"Processing {event_type}: {path}")
        
        # Determine target folder based on path
        if 'Approved' in str(path):
            # File moved to Approved - ready for action
            self._handle_approved_file(path)
        elif 'Incoming' in str(path):
            # New file in Incoming - needs processing
            self._handle_incoming_file(path)
        else:
            logger.debug(f"File in monitored folder: {path}")
    
    def _handle_approved_file(self, path: Path):
        """Handle file moved to Approved folder."""
        logger.info(f"Approved file ready for action: {path}")
        
        # Create processing note
        content = path.read_text() if path.exists() else ""
        
        # Add processing timestamp
        if not self.dry_run:
            timestamp = f"\n\n---\napproved_at: {datetime.now().isoformat()}\nready_for_execution: true\n---"
            # Note: In production, append to file carefully
            logger.info(f"File {path} ready for orchestrator processing")
        else:
            logger.info(f"[DRY RUN] Would process approved file: {path}")
    
    def _handle_incoming_file(self, path: Path):
        """Handle new file in Incoming folder."""
        logger.info(f"Incoming file for processing: {path}")
        
        # Create action file in Needs_Action
        if path.exists():
            content = path.read_text()
            
            # Move to Needs_Action with metadata
            needs_action_path = VAULT_PATH / 'Needs_Action' / f"FILE_{path.name}"
            
            action_content = f"""---
created: {datetime.now().isoformat()}
source: file
original_file: {str(path)}
status: pending
---

# File Received

**Source:** {path}  
**Received:** {datetime.now().isoformat()}

## Content

{content}

## Suggested Actions

<!-- Claude Code will populate this -->

## Processing Log

- [{datetime.now().isoformat()}] Detected by File Watcher
"""
            
            if not self.dry_run:
                needs_action_path.write_text(action_content)
                logger.info(f"Created action file: {needs_action_path}")
            else:
                logger.info(f"[DRY RUN] Would create: {needs_action_path}")
    
    def start(self):
        """Start watching."""
        logger.info("Starting File Watcher...")
        logger.info(f"Monitoring: {INCOMING_PATH}, {APPROVED_PATH}")
        
        # Create handler
        handler = FileChangeHandler(
            callback=self._process_file,
            dry_run=self.dry_run
        )
        
        # Create observer
        self.observer = Observer()
        
        # Watch directories
        self.observer.schedule(handler, str(INCOMING_PATH), recursive=False)
        self.observer.schedule(handler, str(APPROVED_PATH), recursive=False)
        
        # Start
        self.observer.start()
        logger.info("File Watcher started")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("File Watcher stopped")


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='File Watcher')
    parser.add_argument('--dry-run', action='store_true', help='Run without creating files')
    args = parser.parse_args()
    
    watcher = FileWatcher(dry_run=args.dry_run)
    watcher.start()


if __name__ == '__main__':
    main()
