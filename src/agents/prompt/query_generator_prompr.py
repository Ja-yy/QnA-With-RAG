from langchain.prompts import StringPromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from pydantic.v1 import BaseModel, validator, Field
from typing import Callable, List, Optional, Union
from langchain.output_parsers import PydanticOutputParser


class SearchQueryParser(BaseModel):
    main_question: Optional[str] = Field(description="User question")
    search_queries: Optional[List[str]] = Field(
        description="Queries generated to reach further"
    )
    search_queries_count: int = Field(description="Count of generated Queries")


search_query_parser = PydanticOutputParser(pydantic_object=SearchQueryParser)


class QueryGeneratorPromptTemplate(StringPromptTemplate):

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""

        if len(v) != 1 or "question" not in v:
            raise ValueError("question must be the only input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # Generate the prompt to be sent to the language model
        format_instructions = search_query_parser.get_format_instructions()
        prompt = f"""Generate a list of search queries based on the user's question:
1. If the question is a simple greeting or not related to English, return an empty list.
2. For topic-specific questions, identify and search for up to two key terms or phrases relevant to the query. If there are more than two, prioritize the most important/unique ones.
Main Question: {kwargs["question"]}
{format_instructions}"""
        return prompt

    def _prompt_type(self):
        return "query_generator"


query_prompt_template = QueryGeneratorPromptTemplate(
    input_variables=["question"], output_parser=search_query_parser)
