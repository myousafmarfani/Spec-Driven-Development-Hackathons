"""
Watchdog - Health monitor for AI Employee system.

The Watchdog:
1. Monitors all critical processes (watchers, orchestrator)
2. Auto-restarts failed processes
3. Alerts human if processes fail repeatedly
4. Maintains system uptime
"""

import os
import sys
import time
import json
import logging
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger

# Configuration
VAULT_PATH = Path(__file__).parent.parent / 'Vault'
LOGS_PATH = VAULT_PATH / 'Logs'
PID_PATH = Path('/tmp/ai_employee')  # PID files location

# Process definitions
PROCESSES = {
    'orchestrator': {
        'command': 'python src/orchestrator.py',
        'restart_delay': 5,
        'max_restarts_per_hour': 5
    },
    'gmail_watcher': {
        'command': 'python src/watchers/gmail_watcher.py',
        'restart_delay': 5,
        'max_restarts_per_hour': 5
    },
    'whatsapp_watcher': {
        'command': 'python src/watchers/whatsapp_watcher.py',
        'restart_delay': 10,
        'max_restarts_per_hour': 3
    },
    'file_watcher': {
        'command': 'python src/watchers/file_watcher.py',
        'restart_delay': 5,
        'max_restarts_per_hour': 5
    }
}

# Check interval (seconds)
CHECK_INTERVAL = int(os.getenv('WATCHDOG_CHECK_INTERVAL', '30'))

# Alert threshold
ALERT_THRESHOLD = int(os.getenv('WATCHDOG_ALERT_THRESHOLD', '3'))

logger = setup_logger('watchdog', LOGS_PATH)


class ProcessInfo:
    """Track process information."""
    
    def __init__(self, name: str):
        self.name = name
        self.pid: Optional[int] = None
        self.start_time: Optional[datetime] = None
        self.restart_count: int = 0
        self.last_restart: Optional[datetime] = None
        self.restarts_in_hour: List[datetime] = []
    
    def record_restart(self):
        """Record a restart event."""
        self.restart_count += 1
        self.last_restart = datetime.now()
        self.restarts_in_hour.append(self.last_restart)
        
        # Keep only restarts in the last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        self.restarts_in_hour = [
            t for t in self.restarts_in_hour if t > one_hour_ago
        ]
    
    def get_restarts_in_hour(self) -> int:
        """Get number of restarts in the last hour."""
        return len(self.restarts_in_hour)


class Watchdog:
    """Monitor and restart critical processes."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.processes: Dict[str, ProcessInfo] = {}
        self.alerts: List[Dict] = []
        
        # Initialize process tracking
        for name in PROCESSES:
            self.processes[name] = ProcessInfo(name)
        
        # Ensure PID directory exists
        PID_PATH.mkdir(parents=True, exist_ok=True)
    
    def _get_pid_file(self, name: str) -> Path:
        """Get PID file path for a process."""
        return PID_PATH / f"{name}.pid"
    
    def _read_pid(self, name: str) -> Optional[int]:
        """Read PID from file."""
        pid_file = self._get_pid_file(name)
        if not pid_file.exists():
            return None
        
        try:
            return int(pid_file.read_text().strip())
        except (ValueError, IOError):
            return None
    
    def _write_pid(self, name: str, pid: int):
        """Write PID to file."""
        pid_file = self._get_pid_file(name)
        pid_file.write_text(str(pid))
    
    def _remove_pid(self, name: str):
        """Remove PID file."""
        pid_file = self._get_pid_file(name)
        if pid_file.exists():
            pid_file.unlink()
    
    def _is_process_running(self, pid: int) -> bool:
        """Check if a process with given PID is running."""
        if pid is None:
            return False
        
        try:
            # Windows
            if os.name == 'nt':
                result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True,
                    text=True
                )
                return str(pid) in result.stdout
            # Unix/Linux/Mac
            else:
                os.kill(pid, 0)
                return True
        except (OSError, subprocess.SubprocessError):
            return False
    
    def _start_process(self, name: str) -> bool:
        """Start a process."""
        if name not in PROCESSES:
            logger.error(f"Unknown process: {name}")
            return False
        
        config = PROCESSES[name]
        command = config['command']
        
        logger.info(f"Starting {name}: {command}")
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would start {name}")
            return True
        
        try:
            # Start process in background
            if os.name == 'nt':
                # Windows
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=str(Path(__file__).parent.parent),
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                # Unix
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=str(Path(__file__).parent.parent),
                    preexec_fn=os.setsid
                )
            
            # Record PID
            self._write_pid(name, process.pid)
            self.processes[name].pid = process.pid
            self.processes[name].start_time = datetime.now()
            
            logger.info(f"Started {name} with PID {process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start {name}: {e}")
            return False
    
    def _stop_process(self, name: str) -> bool:
        """Stop a process."""
        pid = self._read_pid(name)
        
        if pid is None:
            logger.debug(f"No PID file for {name}")
            return True
        
        if not self._is_process_running(pid):
            logger.debug(f"Process {name} (PID {pid}) not running")
            self._remove_pid(name)
            return True
        
        logger.info(f"Stopping {name} (PID {pid})")
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would stop {name}")
            return True
        
        try:
            if os.name == 'nt':
                # Windows
                subprocess.run(['taskkill', '/PID', str(pid), '/F'], 
                             capture_output=True)
            else:
                # Unix
                os.killpg(os.getpgid(pid), signal.SIGTERM)
                
                # Wait for process to stop
                time.sleep(2)
                
                # Force kill if still running
                if self._is_process_running(pid):
                    os.killpg(os.getpgid(pid), signal.SIGKILL)
            
            self._remove_pid(name)
            logger.info(f"Stopped {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop {name}: {e}")
            return False
    
    def _check_process(self, name: str) -> bool:
        """Check if process is running, restart if needed."""
        pid = self._read_pid(name)
        
        if self._is_process_running(pid):
            logger.debug(f"{name} is running (PID {pid})")
            return True
        
        # Process not running - check if we should restart
        process_info = self.processes[name]
        
        # Check restart limit
        restarts_in_hour = process_info.get_restarts_in_hour()
        max_restarts = PROCESSES[name]['max_restarts_per_hour']
        
        if restarts_in_hour >= max_restarts:
            logger.error(
                f"{name} exceeded restart limit "
                f"({restarts_in_hour}/{max_restarts} per hour)"
            )
            self._create_alert(
                'critical',
                f"Process {name} exceeded restart limit",
                f"Restarted {restarts_in_hour} times in the last hour"
            )
            return False
        
        # Restart process
        logger.warning(f"{name} not running, attempting restart...")
        
        # Wait before restart
        restart_delay = PROCESSES[name]['restart_delay']
        logger.info(f"Waiting {restart_delay}s before restart...")
        time.sleep(restart_delay)
        
        if self._start_process(name):
            process_info.record_restart()
            return True
        
        return False
    
    def _create_alert(self, level: str, title: str, message: str):
        """Create an alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'title': title,
            'message': message
        }
        
        self.alerts.append(alert)
        
        # Log alert
        if level == 'critical':
            logger.critical(f"ALERT: {title} - {message}")
        elif level == 'warning':
            logger.warning(f"ALERT: {title} - {message}")
        else:
            logger.info(f"ALERT: {title} - {message}")
        
        # Write alert to file
        self._write_alerts()
    
    def _write_alerts(self):
        """Write alerts to file."""
        alerts_file = LOGS_PATH / 'alerts.json'
        
        # Keep only last 100 alerts
        recent_alerts = self.alerts[-100:]
        
        with open(alerts_file, 'w') as f:
            json.dump(recent_alerts, f, indent=2)
    
    def _update_dashboard(self):
        """Update dashboard with system health."""
        dashboard_path = VAULT_PATH / 'Dashboard.md'
        
        if not dashboard_path.exists():
            return
        
        content = dashboard_path.read_text()
        
        # Build status table
        status_lines = []
        for name, info in self.processes.items():
            pid = self._read_pid(name)
            running = self._is_process_running(pid)
            status = "✓ Running" if running else "✗ Stopped"
            last_check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            status_lines.append(
                f"| {name} | {status} | {last_check} |"
            )
        
        status_table = "\n".join(status_lines)
        
        # Update placeholders
        content = content.replace(
            '{{WATCHDOG_STATUS}}',
            '✓ Monitoring' if self.alerts else '✓ All systems nominal'
        )
        content = content.replace(
            '{{WATCHDOG_LAST_CHECK}}',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        content = content.replace(
            '{{ALERTS}}',
            '\n'.join([f"- [{a['level']}] {a['title']}: {a['message']}" 
                      for a in self.alerts[-5:]]) or '- No alerts'
        )
        
        # Update system health table
        lines = content.split('\n')
        in_health_table = False
        new_lines = []
        
        for line in lines:
            if '| Component | Status |' in line:
                in_health_table = True
                new_lines.append(line)
            elif in_health_table and line.startswith('|---'):
                new_lines.append(line)
                new_lines.extend(status_lines)
                in_health_table = False
            elif not in_health_table:
                new_lines.append(line)
        
        if not self.dry_run:
            dashboard_path.write_text('\n'.join(new_lines))
    
    def start_all_processes(self):
        """Start all monitored processes."""
        logger.info("Starting all processes...")
        
        for name in PROCESSES:
            pid = self._read_pid(name)
            if not self._is_process_running(pid):
                self._start_process(name)
            else:
                logger.info(f"{name} already running (PID {pid})")
    
    def stop_all_processes(self):
        """Stop all monitored processes."""
        logger.info("Stopping all processes...")
        
        for name in PROCESSES:
            self._stop_process(name)
    
    def run(self):
        """Main watchdog loop."""
        logger.info("=" * 50)
        logger.info("AI Employee Watchdog Starting...")
        logger.info(f"Check interval: {CHECK_INTERVAL}s")
        logger.info(f"Alert threshold: {ALERT_THRESHOLD}")
        logger.info("=" * 50)
        
        # Start all processes
        self.start_all_processes()
        
        try:
            while True:
                # Check each process
                for name in PROCESSES:
                    self._check_process(name)
                
                # Update dashboard
                self._update_dashboard()
                
                # Wait before next check
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Watchdog stopped by user")
            self.stop_all_processes()
        except Exception as e:
            logger.error(f"Watchdog crashed: {e}")
            self.stop_all_processes()
            raise


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Watchdog')
    parser.add_argument('--dry-run', action='store_true', help='Run without starting processes')
    parser.add_argument('--start', action='store_true', help='Start all processes and exit')
    parser.add_argument('--stop', action='store_true', help='Stop all processes and exit')
    parser.add_argument('--status', action='store_true', help='Show process status and exit')
    args = parser.parse_args()
    
    watchdog = Watchdog(dry_run=args.dry_run)
    
    if args.start:
        watchdog.start_all_processes()
        sys.exit(0)
    elif args.stop:
        watchdog.stop_all_processes()
        sys.exit(0)
    elif args.status:
        print("Process Status:")
        print("-" * 40)
        for name in PROCESSES:
            pid = watchdog._read_pid(name)
            running = watchdog._is_process_running(pid)
            status = "Running" if running else "Stopped"
            print(f"  {name}: {status} (PID: {pid})")
        sys.exit(0)
    else:
        watchdog.run()


if __name__ == '__main__':
    main()
