import os
import asyncio
import random
from dotenv import load_dotenv
from agents import Runner, TResponseInputItem
from agent_config import create_agents, get_agent_by_name
from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns
from rich.rule import Rule
from rich.status import Status
from ui import (
    create_header, create_agents_info, create_commands_table,
    display_response, clear_screen, show_help,
    show_goodbye_message, show_error_panel, show_interrupt_message
)
from mem0 import MemoryClient
from user_context import current_user

load_dotenv()
console = Console()

# Initialize Mem0 client
client = MemoryClient()



# API Key validation
if os.getenv('OPENAI_API_KEY'):
    console.print("[green]API Key chargée avec succès[/green]")
else:
    console.print("[red]API Key non trouvée[/red]")
    exit(1)

# Initialize agents
agents = create_agents()


async def main():
    # Setup UI
    clear_screen()
    console.print(create_header())
    console.print()
    console.print(Columns([
        create_agents_info(),
        create_commands_table()
    ], equal=True, expand=True))
    console.print()
    console.print(Rule("[dim]Commencez la conversation ci-dessous[/dim]", style="dim"))
    console.print()
    
    conversation_count = 0
    
    # Get user ID from user input
    console.print("[bold yellow]Configuration initiale[/bold yellow]")
    user_id = Prompt.ask("[cyan]Entrez votre identifiant utilisateur[/cyan]", default=str(random.randint(1, 1000000)))
    
    # Convert to int if it's a number, otherwise keep as string
    try:
        user_id = int(user_id)
    except ValueError:
        pass  # Keep as string if not a number
    
    console.print(f"[green]✓ Identifiant utilisateur: {user_id}[/green]")
   

    console.print()
    
    # Set global user context for memory tools
    current_user.set_user_id(user_id)
    
    filters = {
        "OR": [
            {
                "user_id": user_id
            }
        ]
    }
    memory = client.get_all(user_id=user_id, filters=filters, version="v2")
    print("memory: ", memory)
    
    convo: list[TResponseInputItem] = []
    last_agent = agents["trieur"]

    while True:
        try:
            # Get user input
            user_input = Prompt.ask(
                f"[bold cyan]Moi [/bold cyan] [dim](#{conversation_count + 1})[/dim]"
            ).strip()
            convo.append({"content": user_input, "role": "user"})
            print("Historique de conversation: ", convo)
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print(show_goodbye_message())
                break
            elif user_input.lower() == 'clear':
                clear_screen()
                console.print(create_header())
                console.print()
                continue
            elif user_input.lower() == 'help':
                show_help()
                continue
            elif user_input.lower() == 'agents':
                console.print(create_agents_info())
                continue
            
            if not user_input:
                continue
            
            conversation_count += 1
            print("conversation_count: ", conversation_count)
            
            # Process request
            try:
                with Status("Je réfléchis...", console=console, spinner="dots"):
                    result = await Runner.run(last_agent, convo)
               
                
                #response_text = ""
                #console.print("[dim]🔄 Traitement en cours...[/dim]")
                
                
                #async for event in result.stream_events():
                #    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                #        response_text += event.data.delta
                
                
                # Clear processing message
                console.print("\033[1A\033[K", end="")
                
                # Display response
                if result.final_output:

                    last_agent = result.last_agent
                    
                    display_response(result.last_agent.name, result.final_output) 
                else:
                    console.print(Panel("[red] Aucune réponse reçue[/red]", border_style="red"))
                
            except Exception as processing_error:
              
                console.print(show_error_panel(str(processing_error), "Erreur de traitement"))
                continue
                
            
            convo = result.to_input_list()
            
            
            
            console.print()
           
            
            
        except KeyboardInterrupt:
            console.print(show_interrupt_message())
            break
        except Exception as e:
            console.print(show_error_panel(str(e)))

if __name__ == "__main__":
    asyncio.run(main())