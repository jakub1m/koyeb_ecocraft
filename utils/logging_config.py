import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_execution(func):
    """Decorator that logs entry, exit, and errors in a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        def format_value(val):
            if isinstance(val, str) and len(val) > 20:
                return f"{val[:20]}..."
            elif isinstance(val, (bytes, bytearray)):
                return "<binary data>"
            return val

        filtered_args = tuple(format_value(arg) for arg in args)
        filtered_kwargs = {k: format_value(v) for k, v in kwargs.items()}

        logger.info(f"Entering: {func.__name__} with args: {filtered_args} and kwargs: {filtered_kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting: {func.__name__} with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper
