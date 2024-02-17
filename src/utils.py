from typing import List

from langchain.schema.retriever import BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def create_chunks(files: bytes, knowledge_base: str) -> List[Document]:
    """
    Create Chuck from document

    Args:
    - `file` (bytes) : Uploaded Files
    - `knowledge_base` (str): Name of knowledge base

    Return:
    -`Document` (list) - chunks in Document type
    """
    doc_obj: List[Document] = list()
    for file in files:
        file_content = file.read()
        file_name = file.name

        doc_obj.append(
            Document(
                page_content=file_content,
                metadata={
                    "file_name": file_name,
                    "knowledge_base": knowledge_base,
                },
            )
        )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_documents(doc_obj)
    return chunks


def search_doc(search_queries, retriever: BaseRetriever):
    results = []
    formatted_docs = []
    for q in search_queries.search_queries:
        results.extend(retriever.get_relevant_documents(q))
    for i, doc in enumerate(results):
        doc_string = f"<doc id='{i}'>{doc.page_content}</doc>"
        formatted_docs.append(doc_string)
    return "\n".join(formatted_docs)
