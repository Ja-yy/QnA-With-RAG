"""SETTINGS
Settings loaders using Pydantic BaseSettings classes (load from environment variables / dotenv file)
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
load_dotenv()


class OpenAI(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra='ignore')

    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str
    CHAT_MODEL: str
    TEMPERATURE: int
    MAX_RETRIES: int
    REQUEST_TIMEOUT: int


class ChromaDB(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra='ignore')

    COLLATION_NAME: str
    CHROMADB_HOST: str
    CHROMADB_PORT: str
    CHROMA_SERVER_AUTH_CREDENTIALS: str
    CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER: str
    CHROMA_SERVER_AUTH_PROVIDER: str
    CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER: str


openai_config = OpenAI()
chromadb_config = ChromaDB()
