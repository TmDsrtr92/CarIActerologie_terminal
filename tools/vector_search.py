import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from agents import function_tool

load_dotenv()

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
          embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

          vector_store = Chroma(
              collection_name="traite_de_caracterologie_test",
              embedding_function=embeddings,
              persist_directory="./data/source/vector_stores",
          )

          retriever = vector_store.as_retriever(search_kwargs={"k": k})
          docs = retriever.invoke(query)  # Use invoke() instead of get_relevant_documents()

          # Format results
          results = []
          for i, doc in enumerate(docs, 1):
              content = doc.page_content.strip()
              metadata = doc.metadata if hasattr(doc, 'metadata') else {}
              page = metadata.get('page', 'N/A')
              results.append(f"**Source {i} (Page {page}):**\n{content}\n")
              #print(f"**Source {i} (Page {page}):**\n{content[:200]}...\n")

          return "\n".join(results) if results else "Aucune information trouvée."

      except Exception as e:
          return f"Erreur lors de la recherche: {str(e)}"

# query_test = "Quel est l'effet du défaut de puissance affective chez les sanguins?"
# results = search_caracterologie_knowledge(query_test)
# print(results)