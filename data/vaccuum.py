import chromadb

client = chromadb.PersistentClient(path="./data/source/vector_stores")
collection = client.get_collection(name="la_timidite_v2")
results = collection.get(ids=["page"])["documents"]
print(results) # Not found []