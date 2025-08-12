import getpass
import os
import time
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

file_path = ("data/source/traite_caracterologie-10-30.pdf")

def check_chroma_heartbeat(client, operation_name="operation"):
    """Check if ChromaDB is alive and return heartbeat timestamp"""
    try:
        heartbeat = client.heartbeat()
        print(f"ChromaDB alive during {operation_name} - Heartbeat: {heartbeat}")
        return heartbeat
    except Exception as e:
        print(f"ChromaDB heartbeat failed during {operation_name}: {e}")
        raise Exception(f"ChromaDB connection lost during {operation_name}")

def add_documents_with_heartbeat_monitoring(vector_store, documents, client, batch_size=100, heartbeat_interval=30):
    """Add documents to vector store with periodic heartbeat checks"""
    total_docs = len(documents)
    last_heartbeat_time = time.time()

    print(f"Starting to add {total_docs} documents to vector store...")

    for i in range(0, total_docs, batch_size):
        current_time = time.time()

        # Check heartbeat every heartbeat_interval seconds
        if current_time - last_heartbeat_time >= heartbeat_interval:
            check_chroma_heartbeat(client, f"batch processing ({i+1}-{min(i+batch_size, total_docs)}/{total_docs})")
            last_heartbeat_time = current_time

        # Process batch
        batch = documents[i:i+batch_size]
        try:
            vector_store.add_documents(batch)
            print(f"Added batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} ({len(batch)} documents)")
        except Exception as e:
            print(f"Error adding batch {i//batch_size + 1}: {e}")
            # Check if ChromaDB is still alive
            check_chroma_heartbeat(client, "error recovery")
            raise

# Step 1 - Load the PDF file
print("Step 1: Loading PDF file...")
loader = PyPDFLoader(file_path)
pages = loader.load()

# Step 2 - Split the PDF file into chunks
print("Step 2: Splitting PDF into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2171, chunk_overlap=0)
texts = text_splitter.split_documents(pages)

# Step 3 - Create the vector store
print("Step 3: Setting up vector store...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

try:
    # Initialize ChromaDB client and check initial heartbeat
    chroma_client = chromadb.PersistentClient(path="./temp")
    initial_heartbeat = check_chroma_heartbeat(chroma_client, "initialization")

    # Create vector store
    vector_store = Chroma(
        collection_name="traite_de_caracterologie_test",
        embedding_function=embeddings,
        persist_directory="./temp",
    )

    # Step 4 - Add documents to vector store with heartbeat monitoring
    print("Step 4: Adding documents with heartbeat monitoring...")
    add_documents_with_heartbeat_monitoring(
        vector_store,
        texts,
        chroma_client,
        batch_size=50,  # Smaller batches for more frequent heartbeat checks
        heartbeat_interval=20  # Check heartbeat every 20 seconds
    )

    # Final heartbeat check
    final_heartbeat = check_chroma_heartbeat(chroma_client, "completion")

    print(f"\nVector store created successfully!")
    print(f"Processed {len(pages)} pages")
    print(f"Created {len(texts)} text chunks")
    print(f"Saved to: ./temp")
    print(f"Initial heartbeat: {initial_heartbeat}")
    print(f"Final heartbeat: {final_heartbeat}")
    print(f"Process duration: {(final_heartbeat - initial_heartbeat) / 1_000_000_000:.2f} seconds")
    
    # Step 5 - Test query to retrieve 10 chunks
    print("\nStep 5: Testing query retrieval...")
    test_query = "Qu'est-ce que la caractérologie?"
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    
    retrieved_docs = retriever.get_relevant_documents(test_query)
    print(f"\n🔍 Query: '{test_query}'")
    print(f"📊 Retrieved {len(retrieved_docs)} chunks:")
    print("=" * 80)
    
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"\n📄 Chunk {i}:")
        print(f"Content: {doc.page_content[:500]}...")  # First 200 chars
        if hasattr(doc, 'metadata') and doc.metadata:
            print(f"Metadata: {doc.metadata}")
        print("-" * 40)

except Exception as e:
    print(f"❌ Error creating vector store: {e}")
    try:
        # Try one more heartbeat to see if ChromaDB is still responsive
        check_chroma_heartbeat(chroma_client, "error diagnosis")
    except:
        print("ChromaDB appears to be unresponsive")