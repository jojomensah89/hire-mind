import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        # Create base log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, default=str)


def setup_logging(level: str = "INFO") -> None:
    """Setup structured logging configuration"""
    
    # Create formatter
    formatter = StructuredFormatter()
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    root_logger.propagate = False


def get_auth_logger(name: str) -> logging.Logger:
    """Get a logger specifically configured for authentication operations"""
    logger = logging.getLogger(f"auth.{name}")
    return logger


def log_auth_event(
    logger: logging.Logger,
    event_type: str,
    message: str,
    level: str = "INFO",
    user_id: Optional[str] = None,
    clerk_id: Optional[str] = None,
    event_data: Optional[Dict[str, Any]] = None,
    error_details: Optional[Dict[str, Any]] = None
) -> None:
    """Log authentication events with structured data"""
    
    extra_data = {
        "event_type": event_type,
        "auth_operation": True,
    }
    
    if user_id:
        extra_data["user_id"] = user_id
    
    if clerk_id:
        extra_data["clerk_id"] = clerk_id
    
    if event_data:
        extra_data["event_data"] = event_data
    
    if error_details:
        extra_data["error_details"] = error_details
    
    log_level = getattr(logging, level.upper())
    logger.log(log_level, message, extra=extra_data)


# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)
