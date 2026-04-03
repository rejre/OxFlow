"""
OxFlow - Logging Configuration
Centralized logging setup for the application.
"""

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(
    name: str = "oxflow",
    level: int = logging.INFO,
    log_file: str = None,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Configure logging for OxFlow.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, defaults to ~/.oxflow/logs/oxflow.log
        max_bytes: Max size of log file before rotation (default: 5MB)
        backup_count: Number of backup log files to keep (default: 3)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file is None:
        log_dir = Path.home() / ".oxflow" / "logs"
    else:
        log_dir = Path(log_file).parent
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    if log_file is None:
        log_file = log_dir / "oxflow.log"
    else:
        log_file = Path(log_file)
    
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except (IOError, OSError) as e:
        logger.warning(f"Failed to setup file logging: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger instance."""
    return logging.getLogger(f"oxflow.{name}")


# Global logger setup
_logger = None


def initialize():
    """Initialize global logging configuration."""
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger
