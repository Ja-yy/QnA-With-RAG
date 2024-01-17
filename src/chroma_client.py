from typing import Type

from chromadb import HttpClient
from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma



class BaseChroma:
    def __init__(self) -> None:
        self.embedding_funcation = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY, model_name=EMBEDDING_MODEL
        )
        self.chroma_client = HttpClient(
            host="server",
            port="8000",
        )
        # self.chroma_client = PersistentClient(path="db")

        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY, model=EMBEDDING_MODEL
        )

    @classmethod
    def get_collection(
        cls: Type["BaseChroma"], collection_name: str = COLLATION_NAME
    ) -> Collection:
        """
        Returns the collection with the specified name in Chroma, or creates a new collection if it doesn't exist.

        Returns:
            Collection: The collection with the specified name in Chroma.

        """
        basechroma_inst = cls()
        collection = basechroma_inst.chroma_client.get_or_create_collection(
            embedding_function=basechroma_inst.embeddings, name=collection_name
        )

        return collection

    @classmethod
    def get_vectore_stor(
        cls: Type["BaseChroma"], collection_name: str = COLLATION_NAME
    ):
        basechroma_inst = cls()

        vectordb = Chroma(
            client=basechroma_inst.chroma_client,
            embedding_function=basechroma_inst.embeddings,
            collection_name=collection_name,
        )
        return vectordb.as_retriever(search_kwargs=dict(k=3))
