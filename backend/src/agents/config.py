from openai import OpenAI
import os
from dotenv import load_dotenv
from ..utils.logging import get_logger

load_dotenv()

logger = get_logger("agent-config")

class AgentConfig:
    """
    Configuration for the AI agent using OpenAI-compatible interface with Cohere.
    """

    def __init__(self):
        # Store configuration values but don't initialize client yet
        self._client = None

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

        # Model to use (matching approach in agent_service.py)
        self.model = "command-r-08-2024"  # Using Cohere's command-r model as in agent_service.py

        logger.info("Agent configuration initialized with lazy client initialization")

    def get_client(self):
        """
        Get the OpenAI client configured for Cohere API.
        Initializes the client only when first accessed to avoid startup issues.

        Returns:
            OpenAI client instance
        """
        if self._client is None:
            # Temporarily clear proxy environment variables that may interfere with OpenAI client
            proxy_backup = {}
            for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
                if key in os.environ:
                    proxy_backup[key] = os.environ[key]
                    del os.environ[key]

            try:
                # Get API key from environment variable (matching approach in agent_service.py)
                api_key = os.getenv("COHERE_API_KEY")
                if not api_key:
                    logger.error("No Cohere API key found in environment variables")
                    # Fallback to settings if environment variable is not available
                    from ..config import settings
                    api_key = getattr(settings, 'cohere_api_key', None) or getattr(settings, 'openai_api_key', None)

                if not api_key:
                    raise ValueError("Either COHERE_API_KEY environment variable or settings.cohere_api_key is required")

                # Configure OpenAI client to use Cohere API - using compatibility endpoint like in agent_service.py
                self._client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.cohere.ai/compatibility/v1"  # Use Cohere's compatibility endpoint as in agent_service.py
                )

                logger.info("OpenAI client initialized with Cohere API")

            finally:
                # Restore proxy environment variables if they existed
                for key, value in proxy_backup.items():
                    os.environ[key] = value

        return self._client

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

# Global agent configuration instance (initialized lazily)
_agent_config_instance = None

def get_agent_config() -> AgentConfig:
    """
    Get the global agent configuration instance.

    Returns:
        AgentConfig instance
    """
    global _agent_config_instance
    if _agent_config_instance is None:
        _agent_config_instance = AgentConfig()
    return _agent_config_instance