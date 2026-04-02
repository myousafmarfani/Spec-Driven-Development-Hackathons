"""
Logging utility for the AI Employee system.

Provides consistent logging across all components with:
- File and console output
- JSON formatting for logs
- Log rotation
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName', 
                          'levelname', 'levelno', 'lineno', 'module', 'msecs', 
                          'pathname', 'process', 'processName', 'relativeCreated',
                          'stack_info', 'exc_info', 'exc_text', 'thread', 'threadName']:
                log_entry[key] = value
        
        return json.dumps(log_entry)


class ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter with colors."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return (f"{color}{timestamp} [{record.levelname:8}]{self.RESET} "
                f"{record.name}: {record.getMessage()}")


def setup_logger(name: str, log_path: Path, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name (usually __name__ or module name)
        log_path: Directory to store log files
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Ensure log directory exists
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Log file path
    log_file = log_path / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # File handler (JSON format)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=7,  # Keep 7 days of logs
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(JSONFormatter())
    
    # Console handler (human-readable)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ConsoleFormatter())
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get an existing logger by name."""
    return logging.getLogger(name)


def log_action(log_path: Path, action_type: str, **kwargs):
    """
    Log an action to the audit log.
    
    Args:
        log_path: Path to logs directory
        action_type: Type of action (e.g., 'email_send', 'payment_processed')
        **kwargs: Additional fields to log
    """
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'action_type': action_type,
        'actor': 'ai_employee',
        **kwargs
    }
    
    # Append to daily log file
    log_file = log_path / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl'
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
