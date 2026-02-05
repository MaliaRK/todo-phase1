import asyncio
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sqlmodel import Session
from pydantic import BaseModel
from ..mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task
from ..utils.logging import get_logger
import json
import re

# Disable tracing
os.environ["OPENAI_LOG"] = "none"

load_dotenv()

logger = get_logger("agent-service")

class TaskAgent:
    """
    AI agent for task management using Cohere API directly with MCP tools.
    """

    def __init__(self):
        # Temporarily clear proxy environment variables that may interfere with OpenAI client
        proxy_backup = {}
        for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
            if key in os.environ:
                proxy_backup[key] = os.environ[key]
                del os.environ[key]

        try:
            # Configure AsyncOpenAI client to use Cohere API
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                logger.error("No Cohere API key found in environment variables")
                raise ValueError("COHERE_API_KEY environment variable is required")

            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.cohere.ai/compatibility/v1"  # Use Cohere's compatibility endpoint as in agentbot.py
            )
        finally:
            # Restore proxy environment variables if they existed
            for key, value in proxy_backup.items():
                os.environ[key] = value

        # Agent instructions focused on task management
        self.instructions = """
        You are an AI assistant that helps users manage their todo tasks through natural language.
        Your capabilities include:
        1. Adding new tasks to the user's list
        2. Listing the user's existing tasks
        3. Marking tasks as completed
        4. Deleting tasks from the list
        5. Updating task details

        When a user provides a request, you should:
        - Understand their natural language request
        - Respond with the appropriate function call in JSON format
        - Use the following functions when needed:

        add_task: {"name": "add_task", "arguments": {"user_id": "user_id_string", "title": "task title", "description": "task description (optional)"}}
        list_tasks: {"name": "list_tasks", "arguments": {"user_id": "user_id_string", "status": "all|pending|completed (optional, default: all)"}}
        complete_task: {"name": "complete_task", "arguments": {"user_id": "user_id_string", "task_id": task_id_number}}
        delete_task: {"name": "delete_task", "arguments": {"user_id": "user_id_string", "task_id": task_id_number}}
        update_task: {"name": "update_task", "arguments": {"user_id": "user_id_string", "task_id": task_id_number, "title": "new title (optional)", "description": "new description (optional)"}}

        Format your response as a JSON object with a "function_call" field containing the function to call,
        and a "response" field with a natural language response to the user.
        Example: {"function_call": {"name": "add_task", "arguments": {"user_id": "user123", "title": "Buy groceries"}}, "response": "I've added the task 'Buy groceries' to your list."}
        If no function is needed, just provide the "response" field.
        """

        # Model to use
        self.model = "command-r-08-2024"  # Using Cohere's command-r model as in agentbot.py

        logger.info("TaskAgent initialized with Cohere API and MCP tools")

    async def process_message(self, user_id: str, conversation_id: int, user_message: str) -> Dict[str, Any]:
        """
        Process a user message with the AI agent using Cohere's chat completions API.

        Args:
            user_id: ID of the user sending the message
            conversation_id: ID of the conversation
            user_message: The user's message content

        Returns:
            Dictionary containing the agent's response and any tool calls
        """
        try:
            # Construct the full prompt with instructions and user message
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": user_message}
            ]

            # Call the Cohere API using chat completions
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )

            # Get the response content
            response_content = response.choices[0].message.content

            logger.info(f"Cohere response: {response_content}")

            # Try to parse the response as JSON to see if it contains a function call
            function_call_result = None
            try:
                # Attempt to extract JSON from the response
                json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    response_json = json.loads(json_str)

                    if "function_call" in response_json:
                        function_call = response_json["function_call"]

                        # Execute the function call
                        if function_call["name"] == "add_task":
                            args = function_call["arguments"]
                            # Ensure the correct user ID is used from the API call
                            args["user_id"] = user_id
                            function_call_result = await add_task(
                                user_id=args["user_id"],
                                title=args["title"],
                                description=args.get("description")
                            )
                        elif function_call["name"] == "list_tasks":
                            args = function_call["arguments"]
                            # Ensure the correct user ID is used from the API call
                            args["user_id"] = user_id
                            function_call_result = await list_tasks(
                                user_id=args["user_id"],
                                status=args.get("status", "all")
                            )
                        elif function_call["name"] == "complete_task":
                            args = function_call["arguments"]
                            # Ensure the correct user ID is used from the API call
                            args["user_id"] = user_id
                            function_call_result = await complete_task(
                                user_id=args["user_id"],
                                task_id=int(args["task_id"])
                            )
                        elif function_call["name"] == "delete_task":
                            args = function_call["arguments"]
                            # Ensure the correct user ID is used from the API call
                            args["user_id"] = user_id
                            function_call_result = await delete_task(
                                user_id=args["user_id"],
                                task_id=int(args["task_id"])
                            )
                        elif function_call["name"] == "update_task":
                            args = function_call["arguments"]
                            # Ensure the correct user ID is used from the API call
                            args["user_id"] = user_id
                            function_call_result = await update_task(
                                user_id=args["user_id"],
                                task_id=int(args["task_id"]),
                                title=args.get("title"),
                                description=args.get("description")
                            )

                        # Use the response from the JSON if available
                        if "response" in response_json:
                            response_content = response_json["response"]
                        else:
                            response_content = "Action completed successfully."

            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse JSON from response: {e}. Response: {response_content}")
                # If JSON parsing fails, just return the text response
            except Exception as e:
                logger.error(f"Error executing function call: {str(e)}")
                response_content = "Sorry, I encountered an error processing your request."

            logger.info(f"Processed message for user {user_id}, conversation {conversation_id}")

            return {
                "response": response_content,
                "tool_calls": [{"result": function_call_result}] if function_call_result else [],
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error processing message for user {user_id}, conversation {conversation_id}: {str(e)}")

            return {
                "response": "Sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "status": "error",
                "error": str(e)
            }


# Global agent instance (lazy initialization to avoid startup issues)
_agent_instance = None

def get_agent():
    """
    Get the global agent instance with lazy initialization.

    Returns:
        TaskAgent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TaskAgent()
    return _agent_instance


async def process_user_message(
    user_id: str,
    conversation_id: int,
    user_message: str
) -> Dict[str, Any]:
    """
    Process a user message with the AI agent.

    Args:
        user_id: ID of the user sending the message
        conversation_id: ID of the conversation
        user_message: The user's message content

    Returns:
        Dictionary containing the agent's response and any tool calls
    """
    agent_instance = get_agent()
    return await agent_instance.process_message(user_id, conversation_id, user_message)


async def process_tool_calls(
    tool_calls: List[Dict[str, Any]],
    session: Session
) -> List[Dict[str, Any]]:
    """
    Process the tool calls returned by the agent.

    Args:
        tool_calls: List of tool calls to execute
        session: Database session

    Returns:
        List of results from tool executions
    """
    results = []

    for tool_call in tool_calls:
        try:
            # Results are already processed during agent execution
            results.append({
                "tool_call_id": tool_call["id"],
                "result": tool_call["result"],
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error processing tool call {tool_call['id']}: {str(e)}")
            results.append({
                "tool_call_id": tool_call["id"],
                "result": f"Error: {str(e)}",
                "status": "error"
            })

    return results


async def get_task_summary(user_id: str) -> Dict[str, int]:
    """
    Get a summary of the user's tasks.

    Args:
        user_id: ID of the user

    Returns:
        Dictionary with task counts
    """
    try:
        # Get all tasks for the user
        all_tasks = await list_tasks(user_id=user_id, status="all")
        pending_tasks = await list_tasks(user_id=user_id, status="pending")
        completed_tasks = await list_tasks(user_id=user_id, status="completed")

        return {
            "total_count": len(all_tasks),
            "pending_count": len(pending_tasks),
            "completed_count": len(completed_tasks)
        }
    except Exception as e:
        logger.error(f"Error getting task summary for user {user_id}: {str(e)}")
        return {
            "total_count": 0,
            "pending_count": 0,
            "completed_count": 0
        }