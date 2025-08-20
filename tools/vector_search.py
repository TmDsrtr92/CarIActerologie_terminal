import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from agents import function_tool

load_dotenv()


#client = chromadb.PersistentClient(path="./data/source/vector_stores")
#collection_caracterologie = client.get_collection(name="traite_de_caracterologie_large_v1")
#collection_timidite = client.get_collection(name="la_timidite_v3")


# Initialize once at module level
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store_caracterologie = Chroma(
    collection_name="traite_de_caracterologie_large_v1",
    embedding_function=embeddings,
    persist_directory="./data/source/vector_stores",
)
vector_store_timidite = Chroma(
    collection_name="la_timidite_v3",
    embedding_function=embeddings,
    persist_directory="./data/source/vector_stores",
)


@function_tool
def search_caracterologie_knowledge(query: str, k: int = 5) -> str:
      """
      Search the caractérologie knowledge base for relevant information.
      Args:
          query (str): The query to search for.
          k (int): The number of results to return.
      Returns:
          str: The results of the search.
      """
      try:
          retriever = vector_store_caracterologie.as_retriever(search_kwargs={"k": k})
          docs = retriever.invoke(query)

          # Format results
          results = []
          for i, doc in enumerate(docs, 1):
              content = doc.page_content.strip()
              metadata = doc.metadata if hasattr(doc, 'metadata') else {}
              page = metadata.get('page', 'N/A')
              results.append(f"**Source {i} (Page {page}):**\n{content}\n")

          return "\n".join(results) if results else "Aucune information trouvée."

      except Exception as e:
          return f"Erreur lors de la recherche: {str(e)}"


@function_tool
def search_timidite_knowledge(query: str, k: int = 5) -> str:
      """
      Search the timidité knowledge base for relevant information.
      Args:
          query (str): The query to search for.
          k (int): The number of results to return.
      Returns:
          str: The results of the search.
      """
      try:
          retriever = vector_store_timidite.as_retriever(search_kwargs={"k": k})
          docs = retriever.invoke(query)

          # Format results
          results = []
          for i, doc in enumerate(docs, 1):
              content = doc.page_content.strip()
              metadata = doc.metadata if hasattr(doc, 'metadata') else {}
              page = metadata.get('page', 'N/A')
              results.append(f"**Source {i} (Page {page}):**\n{content}\n")

          return "\n".join(results) if results else "Aucune information trouvée."

      except Exception as e:
          return f"Erreur lors de la recherche: {str(e)}"

"""
query_test = "Quel est l'effet du défaut de puissance affective chez les sanguins?"
results = search_caracterologie_knowledge(query_test)
print(query_test, results)

query_test = "Quels sont les différents types de timides?"
results_timidite = search_timidite_knowledge(query_test)
print(query_test, results_timidite)
"""