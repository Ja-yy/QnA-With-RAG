from bot_stream_llm import StreamChatOpenAI, ThreadedGenerator
from src import agents
from typing import List, Type


class Bot:
    def __init__(self) -> None:
        
        self.stream = ThreadedGenerator()
        self.llm = StreamChatOpenAI(
            gen=self.stream)

        self.agents: List[Type[agents.Agent]] = [
        agents.GreetingAgent,]
        
        self.state.agent_names = [agent.name for agent in self.agents]

        self.agents = [agent(llm=self.llm)
                       for agent in self.agents]