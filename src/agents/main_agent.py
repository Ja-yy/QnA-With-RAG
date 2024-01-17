from src.agents import Agent
from src.bot_stream_llm import StreamChatOpenAI, ThreadedGenerator
import threading


class MainAgent(Agent):
    name = "main_agent"

    def __init__(self):
        self.stream: ThreadedGenerator = ThreadedGenerator()
        self.llm: StreamChatOpenAI = StreamChatOpenAI(
            gen=self.stream)

    def _ask(self,
             raise_exception: bool = False) -> None:

        counter: int = 0
        while True:
            input_req = self.act()
            if input_req is not False:  # continue only if input_req is False
                break
            # Prevent infinite loops.
            counter += 1
            if counter > 5:
                break
        self.stream.close()

    def ask(self, *args, **kwargs):
        # kwargs['raise_exception'] = False
        threading.Thread(target=self._ask, args=args, kwargs=kwargs).start()
        return self.stream

    def act(self) -> bool:
        content = "Hello,What can I do for you?"
        self.llm.stream_callback.on_llm_new_token(content)
        return True
