from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings

client = QdrantClient(host="localhost", port=6333)

embeddings = OpenAIEmbeddings(
    # adjust model name as needed
    model="qwen3-embedding:0.6b",
    # change port to 1234 for LMStudio 
    base_url="http://localhost:11434/v1", 
    # api key only needed for remote servers, otherwise ignored by local setups
    api_key="ollama", 
    check_embedding_ctx_length=False
)

# create collection if it does not exist
if not client.collection_exists("polyu_handbook"):
    # get vector size from the embedding model
    vector_size = len(embeddings.embed_query("sample text"))
    client.create_collection(
        collection_name="polyu_handbook",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="polyu_handbook",
    embedding=embeddings,
)