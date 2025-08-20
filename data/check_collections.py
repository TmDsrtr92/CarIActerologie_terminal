import chromadb

# Connect to the ChromaDB instance
client = chromadb.PersistentClient(path="./data/source/vector_stores")

# Delete a collection
#client.delete_collection(name="la_timidite")

# Modify a collection
# collection = client.get_collection(name="traite_de_caracterologie_large_v1")
#collection.modify(
#   name="traite_de_caracterologie_large_v1",
#   metadata={"description": "First chromaDB collection for the Traité de caracterologie with openAI large embedding model"}
#)



# List all collections
collections = client.list_collections()

print("Available ChromaDB collections:")
print("=" * 40)

if collections:
    for collection in collections:
        print(f"Collection name: {collection.name}")
        print(f"Collection ID: {collection.id}")
        print(f"Collection metadata: {collection.metadata}")
        
        # Get collection info
        try:
            count = collection.count()
            print(f"Document count: {count}")
        except Exception as e:
            print(f"Could not get count: {e}")
        
        print("-" * 30)
else:
    print("No collections found")

print(f"\nTotal collections: {len(collections)}")