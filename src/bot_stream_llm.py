import os
from typing import Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.schema.messages import BaseMessage
from config import openai_config
from src.chroma_client import chroma_db


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class CustomChatOpenAI:
    def __init__(self, **kwargs):
        self.llm_kwargs = kwargs
        self.llm_kwargs["temperature"] = openai_config.TEMPERATURE
        self.llm_kwargs["max_retries"] = openai_config.MAX_RETRIES
        self.llm_kwargs["request_timeout"] = openai_config.REQUEST_TIMEOUT
        self.llm_kwargs["model"] = openai_config.CHAT_MODEL

    def __call__(self, *args, **kwargs: Any) -> BaseMessage:
        que = args[0]
        llm = ChatOpenAI(**self.llm_kwargs)
        llm_result = llm.invoke(que)

        generations_ = llm_result.content

        return generations_


class StreamChatOpenAI:
    def __init__(
        self,
        container,
        **kwargs,
    ):
        self.streaming = os.getenv("STREAMING", "True").lower() == "true"
        self.stream_callback = StreamHandler(container)
        self.llm = CustomChatOpenAI(
            callbacks=[self.stream_callback],
            streaming=self.streaming,
            **kwargs,
        )

    def __call__(self, *args, **kwargs: Any) -> BaseMessage:
        response = self.llm.__call__(*args, **kwargs)
        if not self.streaming:
            self.stream_callback.on_llm_new_token(response.content)
        return response
