import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import os
from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration to be set for the application."""
    LOGGER_NAME: str = "ai-todo-chatbot"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False

def setup_logging() -> logging.Logger:
    """
    Set up logging configuration for the application.

    Returns:
        Configured logger instance
    """
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Create logger
    logger = logging.getLogger("ai-todo-chatbot")
    logger.setLevel(log_level)

    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        "%(levelname)s %(asctime)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Optional name for the logger (defaults to main app logger)

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"ai-todo-chatbot.{name}")
    else:
        return logging.getLogger("ai-todo-chatbot")

def log_api_call(
    logger: logging.Logger,
    endpoint: str,
    method: str,
    user_id: Optional[str] = None,
    response_time: Optional[float] = None,
    status_code: Optional[int] = None
) -> None:
    """
    Log an API call with relevant information.

    Args:
        logger: Logger instance to use
        endpoint: API endpoint that was called
        method: HTTP method used
        user_id: ID of the user making the call (if authenticated)
        response_time: Time taken to process the request (in seconds)
        status_code: HTTP status code of the response
    """
    user_info = f" | User: {user_id}" if user_id else " | User: anonymous"
    response_info = f" | Response time: {response_time:.3f}s" if response_info else ""
    status_info = f" | Status: {status_code}" if status_code else ""

    logger.info(f"API CALL | {method} {endpoint}{user_info}{response_info}{status_info}")

def log_error(
    logger: logging.Logger,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None
) -> None:
    """
    Log an error with context information.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        context: Additional context information
        user_id: ID of the user when error occurred (if applicable)
    """
    context_str = f" | Context: {context}" if context else ""
    user_info = f" | User: {user_id}" if user_id else ""

    logger.error(f"ERROR | {type(error).__name__}: {str(error)}{context_str}{user_info}")

def log_mcp_tool_call(
    logger: logging.Logger,
    tool_name: str,
    user_id: str,
    params: Dict[str, Any],
    success: bool = True,
    execution_time: Optional[float] = None
) -> None:
    """
    Log an MCP tool call with relevant information.

    Args:
        logger: Logger instance to use
        tool_name: Name of the MCP tool called
        user_id: ID of the user triggering the tool
        params: Parameters passed to the tool
        success: Whether the tool call was successful
        execution_time: Time taken to execute the tool (in seconds)
    """
    status = "SUCCESS" if success else "FAILED"
    time_info = f" | Execution time: {execution_time:.3f}s" if execution_time else ""

    logger.info(f"MCP TOOL | {status} | Tool: {tool_name} | User: {user_id} | Params: {params}{time_info}")

# Initialize the main logger when module is imported
main_logger = setup_logging()