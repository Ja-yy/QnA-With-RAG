from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from openai import AuthenticationError
from streamlit import session_state

from src.agents.prompt.main_prompt_templae import main_prompt_template
from src.agents.prompt.query_generator_prompr import (
    query_prompt_template,
    search_query_parser,
)
from src.bot_stream_llm import CustomChatOpenAI, StreamChatOpenAI
from src.chroma_client import BaseChroma
from src.utils import search_doc


class MainAgent:

    def __init__(self, llm: StreamChatOpenAI, knowlwdge_name: str) -> None:
        self.chroma_db = BaseChroma()
        self.llm = llm
        self.retriever = self.chroma_db.get_vector_store(knowlwdge_name)

    def query_chain(self):
        local_llm = CustomChatOpenAI()
        chain_map = {
            "answer": {"question": RunnablePassthrough()}
            | query_prompt_template
            | local_llm
            | search_query_parser,
        }
        return RunnableMap(chain_map)

    def run(self, question: str):
        try:
            _input = self.query_chain()

            _context = {
                "context": lambda x: search_doc(x["answer"], self.retriever),
                "question": RunnablePassthrough(),
            }
            chain = (
                _input | _context | main_prompt_template | self.llm | StrOutputParser()
            )
            result = chain.invoke(question)
            return result
        except AuthenticationError:
            message = "Please enter valid api key!!!"
            session_state.openai_api_key = None
            self.llm.stream_callback.on_llm_new_token(message)
            return message
        except Exception:
            message = "Something went wrong on our end. Please try again later."
            self.llm.stream_callback.on_llm_new_token(message)
