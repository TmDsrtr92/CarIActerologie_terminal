import os
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
from tools.vector_search import search_caracterologie_knowledge
from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich import print as rprint

load_dotenv()

console = Console()

if os.getenv('OPENAI_API_KEY'):
    console.print("✅ API Key loaded successfully", style="green")
else:
    console.print("❌ API Key not found", style="red")

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
    # Welcome banner
    welcome_panel = Panel.fit(
        "[bold blue]🧠 Système de Caractérologie[/bold blue]\n"
        "[dim]Découvrez votre personnalité avec l'IA[/dim]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(welcome_panel)
    
    console.print("[dim]💡 Tapez 'quit' ou 'exit' pour quitter[/dim]")
    console.print("[dim]🔄 L'agent se souviendra automatiquement des messages précédents[/dim]\n")

    while True:
        try:
            # Get user input with rich prompt
            user_input = Prompt.ask("[bold cyan]Vous[/bold cyan]").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print(Panel("👋 [bold yellow]Au revoir![/bold yellow]", border_style="yellow"))
                break

            # Skip empty inputs
            if not user_input:
                continue

            # Show processing with spinner
            with console.status("[bold green]🤔 Analyse en cours...", spinner="dots"):
                result = Runner.run_streamed(caracteriologue_agent, user_input)
                
                # Collect response text
                response_text = ""
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        response_text += event.data.delta

            # Display the response in a beautiful panel
            if result.final_output:
                response_panel = Panel(
                    Markdown(result.final_output),
                    title="[bold green]🤖 Caractériologue[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print(response_panel)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Au revoir![/yellow]")
            break
        except Exception as e:
            error_panel = Panel(
                f"[bold red]❌ Erreur:[/bold red] {e}",
                border_style="red"
            )
            console.print(error_panel)

if __name__ == "__main__":
    asyncio.run(main())