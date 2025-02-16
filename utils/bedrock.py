import boto3
from enum import Enum, auto
from typing import Any

from utils.settings import CONFIG


class AgentType(Enum):
    QA = auto()


class BedrockAgent:
    
    _config: dict[str, Any] = CONFIG

    def __init__(
        self,
        agent_type: AgentType,
        max_tokens: int = 1_000,
    ) -> None:
        self.client = boto3.client("bedrock-runtime")
        self.model_id = self._config["Models"]["Base"]
        self.agent_type = agent_type
        self.max_tokens = max_tokens

        self._system_prompt: str

        if agent_type == AgentType.QA:
            self._system_prompt = self._config["Prompts"]["System"]["QA"]
        else:
            raise ValueError(f"Agent type {agent_type} not supported")
        

    def answer(
        self,
        question: str,
    ) -> str:
        user_content: list[dict[str, Any]] = [
            {"text": question},
        ]

        messages = [
            {
                "role": "assistant",
                "content": [{"text": self._system_prompt}],
            },
            {
                "role": "user",
                "content": user_content,
            }
        ]

        response = self.client.converse(
            modelId=self.model_id,
            messages=messages,
            inferenceConfig={"maxTokens": self.max_tokens},
        )

        generated_test: str = response["output"]["message"]["content"][0]["text"]

        return generated_test
