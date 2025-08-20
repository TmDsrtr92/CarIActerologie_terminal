import chromadb

client = chromadb.PersistentClient(path="./data/source/vector_stores")

client.delete_collection(name="la_timidite_v1")

# List all collections
collections = client.list_collections()

print(collections)