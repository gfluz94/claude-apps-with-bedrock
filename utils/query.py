from string import Template

from utils.bedrock import AgentType
from utils.settings import CONFIG


def build_query(agent_type: AgentType, question: str) -> str:
    if agent_type == AgentType.QA:
        prompt_template = Template(CONFIG["Prompts"]["User"]["QA"])
        query = prompt_template.substitute(question=question)
    elif agent_type == AgentType.IMAGE:
        prompt_template = Template(CONFIG["Prompts"]["User"]["IMAGE"])
        query = prompt_template.substitute(question=question)
    else:
        raise ValueError(f"Agent type {agent_type} not supported.")
    return query
