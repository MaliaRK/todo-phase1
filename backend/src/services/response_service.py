from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..utils.logging import get_logger
from ..services.agent_service import get_task_summary

logger = get_logger("response-service")

class ToolCall(BaseModel):
    """
    Model for tool calls in the response.
    """
    id: str
    type: str = "function"
    function: Dict[str, Any]


class TaskSummary(BaseModel):
    """
    Model for task summary in the response.
    """
    total_count: int
    pending_count: int
    completed_count: int


async def format_response(
    agent_response: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Format the agent's response for the API.

    Args:
        agent_response: Raw response from the agent

    Returns:
        Formatted response dictionary
    """
    try:
        # Extract the main response
        response_text = agent_response.get("response", "")

        # Format tool calls if they exist
        raw_tool_calls = agent_response.get("tool_calls", [])
        formatted_tool_calls = []

        for raw_call in raw_tool_calls:
            formatted_tool_call = {
                "id": raw_call.get("id", ""),
                "type": "function",
                "function": {
                    "name": raw_call.get("name", ""),
                    "arguments": raw_call.get("arguments", "{}")
                }
            }
            formatted_tool_calls.append(formatted_tool_call)

        # Get task summary if user_id is available
        task_summary = None
        if "user_id" in agent_response:
            user_id = agent_response["user_id"]
            task_counts = await get_task_summary(user_id)
            task_summary = TaskSummary(
                total_count=task_counts["total_count"],
                pending_count=task_counts["pending_count"],
                completed_count=task_counts["completed_count"]
            )

        # Create the formatted response
        formatted_response = {
            "response": response_text,
            "tool_calls": formatted_tool_calls,
            "task_summary": task_summary.dict() if task_summary else None,
            "status": agent_response.get("status", "success")
        }

        logger.info("Response formatted successfully")
        return formatted_response

    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")

        # Return a safe fallback response
        return {
            "response": "I processed your request.",
            "tool_calls": [],
            "task_summary": None,
            "status": "error",
            "error": str(e)
        }


async def create_error_response(
    error_message: str,
    user_message: str = "",
    conversation_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create an error response for the API.

    Args:
        error_message: The error message to include in the response
        user_message: The original user message (for context)
        conversation_id: The conversation ID (if available)

    Returns:
        Error response dictionary
    """
    try:
        response = {
            "conversation_id": conversation_id,
            "response": f"I'm sorry, but I encountered an error: {error_message}. Could you please rephrase your request?",
            "tool_calls": [],
            "task_summary": None,
            "status": "error"
        }

        logger.warning(f"Created error response: {error_message}")

        return response

    except Exception as e:
        logger.error(f"Error creating error response: {str(e)}")
        return {
            "response": "I'm sorry, but I encountered an error processing your request.",
            "tool_calls": [],
            "task_summary": None,
            "status": "error"
        }


async def create_success_response(
    response_text: str,
    conversation_id: int,
    tool_calls: Optional[List[Dict[str, Any]]] = None,
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a success response for the API.

    Args:
        response_text: The response text from the agent
        conversation_id: The conversation ID
        tool_calls: Any tool calls that were made
        user_id: The user ID (to get task summary)

    Returns:
        Success response dictionary
    """
    try:
        # Format tool calls
        formatted_tool_calls = []
        if tool_calls:
            for call in tool_calls:
                formatted_call = {
                    "id": call.get("id", ""),
                    "type": "function",
                    "function": {
                        "name": call.get("name", ""),
                        "arguments": call.get("arguments", "{}")
                    }
                }
                formatted_tool_calls.append(formatted_call)

        # Get task summary if user_id is provided
        task_summary = None
        if user_id:
            task_counts = await get_task_summary(user_id)
            task_summary = TaskSummary(
                total_count=task_counts["total_count"],
                pending_count=task_counts["pending_count"],
                completed_count=task_counts["completed_count"]
            )

        response = {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": formatted_tool_calls,
            "task_summary": task_summary.dict() if task_summary else None,
            "status": "success"
        }

        logger.info(f"Created success response for conversation {conversation_id}")

        return response

    except Exception as e:
        logger.error(f"Error creating success response: {str(e)}")
        return await create_error_response(str(e))


async def enrich_response_with_context(
    response: Dict[str, Any],
    user_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Enrich the response with additional context.

    Args:
        response: The response to enrich
        user_context: Additional context information

    Returns:
        Enriched response dictionary
    """
    try:
        enriched_response = response.copy()

        # Add any relevant context from user_context
        if "user_preferences" in user_context:
            enriched_response["user_preferences"] = user_context["user_preferences"]

        if "last_interaction" in user_context:
            enriched_response["last_interaction"] = user_context["last_interaction"]

        logger.debug("Response enriched with context")
        return enriched_response

    except Exception as e:
        logger.error(f"Error enriching response with context: {str(e)}")
        return response  # Return original response if enrichment fails