from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
#from langchain_ollama import OllamaEmbeddings
import os


client = QdrantClient(host="localhost", port=6333)
embeddings = OpenAIEmbeddings(
    model="qwen3-embedding:0.6b", 
    base_url="http://localhost:11434/v1", 
    api_key="ollama", 
    check_embedding_ctx_length=False
)
# embeddings = OpenAIEmbeddings()
vector_size = len(embeddings.embed_query("sample text"))

if not client.collection_exists("polyu_handbook"):
    client.create_collection(
        collection_name="polyu_handbook",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="polyu_handbook",
    embedding=embeddings,
)