import numpy as np
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable, StringVariable
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import os

# Environment variables for Qdrant connection
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", 6333)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)  # Optional API key
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "omnibot_store")

# Initialize Qdrant client
if QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY
    )
else:
    qdrant_client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT
    )

# Get collection info to understand the structure
collection_info = qdrant_client.get_collection(COLLECTION_NAME)
print(f"Collection info: {collection_info}")

# Scroll through a few points to understand the data structure
sample_points = qdrant_client.scroll(
    collection_name=COLLECTION_NAME,
    limit=5,
    with_vectors=True,
    with_payload=True
)

if not sample_points[0]:
    raise ValueError(f"No points found in collection '{COLLECTION_NAME}'")

# Get the first point to understand the structure
sample_point = sample_points[0][0]
print(f"Sample point: {sample_point}")

# Get vector dimension from the first point
embeds_length = len(sample_point.vector)
print(f"Vector dimension: {embeds_length}")

# Get metadata keys from the first point's payload
meta_keys = list(sample_point.payload.keys()) if sample_point.payload else []
print(f"Metadata keys: {meta_keys}")

# Create Orange Data Mining domain
variable_headers = [ContinuousVariable(f'Dim{index}') for index in range(0, embeds_length)]
metas_headers = [StringVariable(key) for key in meta_keys]
domain = Domain(variable_headers, metas=metas_headers)

# Initialize numpy arrays for vectors and metadata
vectors = np.empty((0, embeds_length), dtype=float)
metas = np.empty((0, len(meta_keys)), dtype='<U256')  # Increased size for longer strings

# Scroll through all points in the collection
offset = None
all_points = []

while True:
    # Scroll through points in batches
    points, next_offset = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        limit=100,  # Batch size
        offset=offset,
        with_vectors=True,
        with_payload=True
    )
    
    if not points:
        break
    
    all_points.extend(points)
    offset = next_offset
    
    if next_offset is None:
        break

print(f"Total points retrieved: {len(all_points)}")

# Process all points
for point in all_points:
    print(f"Processing point ID: {point.id}")
    
    # Add vector to vectors array
    vector = np.array(point.vector).reshape(1, -1)
    vectors = np.vstack([vectors, vector])
    
    # Add metadata to metas array
    if meta_keys:
        meta_values = []
        for key in meta_keys:
            value = point.payload.get(key, "") if point.payload else ""
            # Convert value to string and handle None values
            meta_values.append(str(value) if value is not None else "")
        
        meta_row = np.array(meta_values).reshape(1, -1)
        metas = np.vstack([metas, meta_row])
    else:
        # If no metadata, create empty row
        empty_row = np.array([""]).reshape(1, 1)
        metas = np.vstack([metas, empty_row])

# Create Orange Table from the data
if meta_keys:
    out_data = Table.from_numpy(domain, vectors, metas=metas)
else:
    out_data = Table.from_numpy(domain, vectors)

print(f"Created Orange table with {len(out_data)} rows and {len(out_data.domain.attributes)} features")
print(f"Metadata columns: {[attr.name for attr in out_data.domain.metas]}")

# Optional: Save the table to a file
# out_data.save("qdrant_data.tab")