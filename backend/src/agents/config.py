from openai import OpenAI
import os
from dotenv import load_dotenv
from ..config import settings
from ..utils.logging import get_logger

load_dotenv()

logger = get_logger("agent-config")

class AgentConfig:
    """
    Configuration for the AI agent using OpenAI-compatible interface with Cohere.
    """

    def __init__(self):
        # Configure OpenAI client to use Cohere API
        self.client = OpenAI(
            api_key=settings.cohere_api_key or settings.openai_api_key,
            base_url="https://api.cohere.ai/v1"  # Use Cohere's OpenAI-compatible endpoint
        )

        # Agent instructions focused on task management
        self.agent_instructions = """
        You are an AI assistant that helps users manage their todo tasks through natural language.
        Your capabilities include:
        1. Adding new tasks to the user's list
        2. Listing the user's existing tasks
        3. Marking tasks as completed
        4. Deleting tasks from the list
        5. Updating task details

        When a user provides a request, you should:
        - Understand their natural language request
        - Select the appropriate tool from the available tools
        - Execute the tool with the correct parameters
        - Provide a friendly response to the user confirming the action or providing the requested information

        Always be helpful, clear, and concise in your responses.
        If you're unsure about any details, ask the user for clarification.
        """

        # Model to use
        self.model = "command-r-plus"  # Using Cohere's command-r-plus model

        logger.info("Agent configuration initialized with Cohere API")

    def get_client(self):
        """
        Get the OpenAI client configured for Cohere API.

        Returns:
            OpenAI client instance
        """
        return self.client

    def get_instructions(self):
        """
        Get the agent instructions.

        Returns:
            String containing agent instructions
        """
        return self.agent_instructions

    def get_model(self):
        """
        Get the model name to use.

        Returns:
            String containing model name
        """
        return self.model

# Global agent configuration instance
agent_config = AgentConfig()

def get_agent_config() -> AgentConfig:
    """
    Get the global agent configuration instance.

    Returns:
        AgentConfig instance
    """
    return agent_config