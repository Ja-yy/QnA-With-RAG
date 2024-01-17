from abc import ABC, abstractmethod
from src.bot_stream_llm import StreamChatOpenAI

class Agent(ABC):
    """
    Base class for creating ChatGPT agents for different purposes.
    """
    name: str

    @abstractmethod
    def __init__(self,llm: StreamChatOpenAI):
        pass

    @abstractmethod
    def act(self) -> bool:
        pass
