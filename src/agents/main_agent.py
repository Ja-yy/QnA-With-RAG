
from src.bot_stream_llm import CustomChatOpenAI
from src.agents.prompt.query_generator_prompr import query_prompt_template, search_query_parser
from src.utils import search_doc

from src.agents.prompt.main_prompt_templae import main_prompt_template
from src.chroma_client import chroma_db
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

from langchain.schema.output_parser import StrOutputParser


class MainAgent:

    def __init__(self, llm: CustomChatOpenAI, knowlwdge_name: str) -> None:
        self.llm = llm
        self.retriever = chroma_db.get_vectore_store(knowlwdge_name)

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

        _input = self.query_chain()

        _context = {
            "context": lambda x: search_doc(x["answer"], self.retriever),
            "question": RunnablePassthrough()
        }
        chain = _input | _context | main_prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(question)
        return result

    # def run(self,question:str):

    #     local_llm = CustomChatOpenAI()

    #     query_prompt = query_prompt_template.format(question=question)

    #     # search queires
    #     query_response = local_llm(query_prompt)
    #     output_parser = search_query_parser.parse(
    #         query_response)  # search_queries
    #     context = search_doc(output_parser, self.retriever)

    #     main_prompt = main_prompt_template.format(question=question,context=context)
    #     response = self.llm.__call__(main_prompt)
    #     return response
