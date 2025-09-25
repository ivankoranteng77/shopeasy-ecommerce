import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger
logger = logging.getLogger("ecommerce_api")


def log_info(message: str, extra_data: dict = None):
    """Log info message with optional extra data."""
    if extra_data:
        logger.info(f"{message} | Data: {extra_data}")
    else:
        logger.info(message)


def log_error(message: str, error: Exception = None, extra_data: dict = None):
    """Log error message with optional exception and extra data."""
    error_msg = message
    if error:
        error_msg += f" | Error: {str(error)}"
    if extra_data:
        error_msg += f" | Data: {extra_data}"
    logger.error(error_msg)


def log_warning(message: str, extra_data: dict = None):
    """Log warning message with optional extra data."""
    if extra_data:
        logger.warning(f"{message} | Data: {extra_data}")
    else:
        logger.warning(message)