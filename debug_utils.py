import os
import logging
from functools import wraps

# Configure debug mode from environment variable
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Set environment variables to suppress HTTP logs when not in debug mode
if not DEBUG_MODE:
    os.environ['HTTPX_LOG_LEVEL'] = 'WARNING'
    os.environ['OPENAI_LOG_LEVEL'] = 'WARNING'

# Configure logging
if DEBUG_MODE:
    logging.basicConfig(
        level=logging.DEBUG,
        format='[DEBUG] %(message)s'
    )
else:
    # In production mode, suppress all logs below WARNING level
    logging.basicConfig(
        level=logging.WARNING,
        format='%(message)s'
    )
    
    # Suppress HTTP request logs from various libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("openai._client").setLevel(logging.WARNING)
    logging.getLogger("openai.resources").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def debug_print(*args, **kwargs):
    """Print debug messages only when DEBUG_MODE is enabled"""
    if DEBUG_MODE:
        print(*args, **kwargs)

def debug_log(message):
    """Log debug messages using the logging system"""
    if DEBUG_MODE:
        logger.debug(message)

def debug_function(func):
    """Decorator to add debug logging to function calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DEBUG_MODE:
            print(f"[DEBUG] Calling {func.__name__} with args: {args[:2]}...")  # Limit args display
        result = func(*args, **kwargs)
        if DEBUG_MODE:
            print(f"[DEBUG] {func.__name__} completed")
        return result
    return wrapper