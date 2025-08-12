import os
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
from tools.vector_search import search_caracterologie_knowledge
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

print("API Key loaded:", bool(os.getenv('OPENAI_API_KEY')))

caracteriologue_agent = Agent(
    name="Caractériologue",
    instructions="Tu aide les utilisateurs à connaitre leur caractère. Tu réponds en français. Tu te présentes en tant que Caractériologue. Tu utilises l'outil search_caracterologie_knowledge pour trouver les informations dans la base de données.",
    model="gpt-4.1-mini",
    tools=[search_caracterologie_knowledge]
)

interrogateur_agent = Agent(
    name="Interrogateur",
    instructions="Tu poses des questions à l'utilisateur pour connaitre son caractère. Tu réponds en français. Tu te présentes en tant que Interrogateur.",
    model="gpt-4.1-mini"
)

trieur_agent = Agent(
    name="Trieur",
    instructions="Tu détermines quel agent utiliser en fonction de la question de l'utilisateur",
    handoffs=[caracteriologue_agent, interrogateur_agent],
    model="gpt-4o-mini"
)

async def main():
      print("================================================")
      print("Système de Caractérologie - Démarré")
      print("================================================")
      print("Tapez 'quit' ou 'exit' pour quitter\n")
      print("L'agent se souviendra automatiquement des messages précédents.\n")
     

      while True:
          try:
              # Get user input
              user_input = input("Vous: ").strip()

              # Check for exit commands
              if user_input.lower() in ['quit', 'exit', 'q']:
                  print("Au revoir!")
                  break

              # Skip empty inputs
              if not user_input:
                  continue

              # Process the query in streamed mode
              print("Traitement en cours...")
              result = Runner.run_streamed(caracteriologue_agent, user_input)
              async for event in result.stream_events():
                  if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

              # Display the response
              print(f"Assistant: {result.final_output}\n")

          except KeyboardInterrupt:
              print("\n Au revoir!")
              break
          except Exception as e:
              print(f" Erreur: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())