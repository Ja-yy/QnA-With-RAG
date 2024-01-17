import os
import re
import queue
import json
from typing import Any, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import ChatGeneration
from langchain.schema.messages import BaseMessage, ChatMessage


class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(
        self,
        data: str,
        chunked: bool
    ):
        content = json.dumps(
            {
                "content": data,
                "chunk": chunked,
            }
        )
        self.queue.put(content)

    def close(self):
        self.queue.put(StopIteration)


class StreamCallback(BaseCallbackHandler):
    def __init__(self, gen: ThreadedGenerator):
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs) -> None:

        contents = re.split(r"(\s+)", token)
        for data in contents:
            self.gen.send(data, chunked=True)

    def send_data_with_props(
        self,
        data: str = "",
        chunked: bool = False,
    ) -> None:
        self.gen.send(
            data,
            chunked=chunked,
        )

    @property
    def ignore_retry(self) -> bool:
        return True


class CustomChatOpenAI:
    def __init__(self, **kwargs):
        self.llm_kwargs = kwargs
        self.llm_kwargs["temperature"] = 0
        self.llm_kwargs["max_retries"] = 2
        self.llm_kwargs["request_timeout"] = 15
        self.llm_kwargs["model"] = "gpt-3.5-turbo"

    def __call__(self, **kwargs: Any) -> BaseMessage:

        llm = ChatOpenAI(**self.llm_kwargs)

        llm_result = llm.generate(**kwargs)

        generations_ = llm_result.generations[0][0]

        # check if generations_ is of type ChatGeneration
        if isinstance(generations_, ChatGeneration):
            # typecast to ChatGeneration
            response = generations_.message
        else:
            response = generations_.text
        return response


class StreamChatOpenAI:
    def __init__(
        self,
        gen: ThreadedGenerator = ThreadedGenerator(),
        **kwargs,
    ):
        self.streaming = os.getenv("STREAMING", "True").lower() == "true"
        self.stream_callback = StreamCallback(
            gen=gen)
        self.llm = CustomChatOpenAI(
            callbacks=[self.stream_callback],
            streaming=self.streaming,
            **kwargs,
        )
