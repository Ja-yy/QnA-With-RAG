from typing import Type, List

from chromadb import HttpClient
from chromadb.config import Settings
from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from config import chromadb_config, openai_config
from langchain_core.vectorstores import VectorStoreRetriever
from chromadb.api import ClientAPI
import streamlit as st
import re


class BaseChroma:
    def __init__(self) -> None:
        self.embedding_funcation = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_config.OPENAI_API_KEY, model_name=openai_config.EMBEDDING_MODEL
        )
        self.chroma_client: ClientAPI = HttpClient(
            host=chromadb_config.CHROMADB_HOST,
            port=chromadb_config.CHROMADB_PORT,
            settings=Settings(chroma_client_auth_provider="token",
                              chroma_client_auth_credentials=chromadb_config.CHROMA_SERVER_AUTH_CREDENTIALS),
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_config.OPENAI_API_KEY, model=openai_config.EMBEDDING_MODEL
        )
        self.collection_name: str = chromadb_config.COLLATION_NAME

    @property
    def default_collection(self):
        return self.chroma_client.get_or_create_collection(
            embedding_function=self.embedding_funcation, name=self.collection_name)

    def _create_collection(self, new_collection_name: str = "default") -> Collection:
        try:
            self.chroma_client.create_collection(
                embedding_function=self.embedding_funcation, name=new_collection_name
            )
            st.success(f"New knowledge {new_collection_name} created")
        except:
            st.warning("Enter valid knowledge base name")

    def _get_collection(self, new_collection_name: str) -> Collection:
        try:
            rtn_coll = self.chroma_client.get_collection(
                embedding_function=self.embedding_funcation, name=new_collection_name
            )
            return rtn_coll
        except:
            return "Collection not found!!!"

    def get_vectore_store(self, collection_name: str) -> VectorStoreRetriever:
        vectordb = Chroma(
            client=self.chroma_client,
            embedding_function=self.embeddings,
            collection_name=collection_name,
        )
        return vectordb.as_retriever(search_kwargs=dict(k=3))

    def create_embeddings(self, documents: List, collection_name: str) -> List[str]:
        """
        Creates embeddings for the given list of documents using the OpenAIEmbeddings API and stores them in Chroma.

        Args:
            documents (List): A list of documents to generate embeddings for.

        Returns:
            ChromaStore: An instance of ChromaStore that represents the collection of embeddings stored in Chroma.
        """
        vector_store = self.get_vectore_store(collection_name)
        doc_store_ids = vector_store.add_documents(documents=documents)
        return doc_store_ids

    def get_knowledge_base_list(self):
        collection_res = self.chroma_client.list_collections()
        unique_knowledge_bases = set(coll.name for coll in collection_res)
        return unique_knowledge_bases

    def get_file_names(self, knowledge_base_name: str):
        try:
            collection_res = self._get_collection(knowledge_base_name)
            file_list = collection_res.get(
                where={"knowledge_base": knowledge_base_name}, include=["metadatas"])
            result_dict = {i: {"id": id_value, "file_name": metadata["file_name"], "knowledge_base": metadata["knowledge_base"]}
                           for i, (id_value, metadata) in enumerate(zip(file_list["ids"], file_list["metadatas"]))
                           if id_value not in set(file_list["ids"][:i])}
            return result_dict
        except ValueError:
            return "No collection found"

    def delete_knowledge_base(self, knowledge_base_name: str = "default"):
        try:
            self.chroma_client.delete_collection(knowledge_base_name)
        except ValueError:
            return "Something went wrong"

    def delete_files_from_knowledge_base(self, knowledge_base_name: str, file_name: List[str]):
        collection_res = self._get_collection(knowledge_base_name)
        try:
            for file in file_name:
                collection_res.delete(where={"file_name": file})
        except:
            st.warning("Something went wrong!!!")


chroma_db = BaseChroma()
