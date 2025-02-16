from utils.bedrock import BedrockAgent, AgentType

if __name__ == "__main__":
    agent = BedrockAgent(agent_type=AgentType.QA)
    response = agent.answer("What is the meaning of life?")
