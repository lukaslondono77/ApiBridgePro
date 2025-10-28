"""
Logging Configuration - Set up sanitized logging
"""
import logging
import sys

from .log_sanitizer import sanitize_log_record


class SanitizeFilter(logging.Filter):
    """Filter to sanitize sensitive data from log records"""

    def filter(self, record: logging.LogRecord) -> bool:
        sanitize_log_record(record)
        return True


def setup_logging(log_level: str = "INFO", sanitize: bool = True) -> None:
    """
    Configure logging with optional sanitization.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        sanitize: Enable log sanitization (default: True)
    """
    # Remove default handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add sanitization filter
    if sanitize:
        console_handler.addFilter(SanitizeFilter())

    # Configure root logger
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    root_logger.addHandler(console_handler)

    # Suppress noisy logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

