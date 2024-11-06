from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_community.embeddings import OllamaEmbeddings
import weaviate
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "mxbai-embed-large")
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = os.getenv("WEAVIATE_PORT", 8080)
WEAVIATE_GRPC_PORT = os.getenv("WEAVIATE_GRPC_PORT", 50051)
INDEX_NAME = os.getenv("INDEX_NAME", "omnibot_store")

weaviate_client = weaviate.connect_to_custom(
        http_host=WEAVIATE_HOST,
        http_port=WEAVIATE_PORT,
        http_secure=False,
        grpc_host=WEAVIATE_HOST,
        grpc_port=WEAVIATE_GRPC_PORT,
        grpc_secure=False,
    )

vectorstore = WeaviateVectorStore(
        client = weaviate_client,
        index_name=INDEX_NAME,
        text_key="page_content",
        embedding=OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_URL),
    )