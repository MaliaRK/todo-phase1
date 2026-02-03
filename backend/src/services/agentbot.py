from dataclasses import dataclass
from typing import Any
from agents import Agent, FunctionTool, ModelSettings, RunContextWrapper, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, enable_verbose_stdout_logging, function_tool, handoff, set_tracing_disabled
from agents.run import RunConfig
import os
#from rich import print
from dotenv import load_dotenv
from pydantic import BaseModel
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.agent import StopAtTools


set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()
load_dotenv()

external_client = AsyncOpenAI(
    api_key=os.getenv("COHERE_API_KEY"),
    base_url= "https://api.cohere.ai/compatibility/v1"
)


model = OpenAIChatCompletionsModel(
    model="command-r-08-2024",
    openai_client=external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
)


triage_agent = Agent(
    name="Triage agent",
    instructions="you are a helpful assistant",
    #handoffs=[billing_agent, handoff_obj, shipping_agent],
    #tools=[get_weather],
    #tool_use_behavior=["run_llm_again"],
    #tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"]),
    #model_settings=ModelSettings(tool_choice="required"),
    #reset_tool_choice=True            # to prevent infinite loop
    )

result = Runner.run_sync(triage_agent, "who is the founder of Pakitan? ", run_config=config)

print(result.final_output)