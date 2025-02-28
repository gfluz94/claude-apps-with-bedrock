from string import Template

from utils.bedrock import AgentType
from utils.settings import CONFIG


def build_query(
    agent_type: AgentType,
    question: str,
    context: str | None = None,
) -> str:
    if agent_type == AgentType.QA:
        prompt_template = Template(CONFIG["Prompts"]["User"]["QA"])
        query = prompt_template.substitute(question=question)
    elif agent_type == AgentType.RAG:
        prompt_template = Template(CONFIG["Prompts"]["User"]["RAG"])
        if context is None:
            raise ValueError("RAG requires context")
        query = prompt_template.substitute(
            question=question,
            context=context,
        )
    elif agent_type == AgentType.IMAGE:
        prompt_template = Template(CONFIG["Prompts"]["User"]["IMAGE"])
        query = prompt_template.substitute(question=question)
    else:
        raise ValueError(f"Agent type {agent_type} not supported.")
    return query
