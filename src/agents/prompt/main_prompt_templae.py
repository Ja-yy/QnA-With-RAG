from typing import Any
from langchain.prompts import StringPromptTemplate
from pydantic.v1 import BaseModel, validator, Field


class MainChainPromptTemplate(StringPromptTemplate, BaseModel):

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        if len(v) != 2 or "context" not in v or "question" not in v:
            raise ValueError(
                "context and question must be the only input_variables.")
        return v

    def format(self, **kwargs) -> str:
        # Generate the prompt to be sent to the language model
        prompt = f"""Answer the question based on the context below. \
            If the user's question is a simple greeting, greet them.\
            If the question cannot be answered using the information provided answer with "I don't know".

Context: {kwargs['context']}
Question: {kwargs['question']}"""
        return prompt

    def _prompt_type(self):
        return "main_chain"


main_prompt_template = MainChainPromptTemplate(
    input_variables=["context", "question"])
