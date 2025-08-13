import os
import asyncio
from dotenv import load_dotenv
from agents import Runner, TResponseInputItem
from agent_config import create_agents, get_agent_by_name
from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns
from rich.rule import Rule
from ui import (
    create_header, create_agents_info, create_commands_table,
    display_response, show_thinking_message, clear_screen, show_help,
    show_goodbye_message, show_error_panel, show_interrupt_message
)

load_dotenv()
console = Console()

# API Key validation
if os.getenv('OPENAI_API_KEY'):
    console.print("[green]API Key chargée avec succès[/green]")
else:
    console.print("[red]API Key non trouvée[/red]")
    exit(1)

# Initialize agents
agents = create_agents()

# Create a session instance with a session ID

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
    
    convo: list[TResponseInputItem] = []
    last_agent = agents["trieur"]

    while True:
        try:
            # Get user input
            user_input = Prompt.ask(
                f"[bold cyan]💬 Moi [/bold cyan] [dim](#{conversation_count + 1})[/dim]"
            ).strip()
            convo.append({"content": user_input, "role": "user"})
            #print("Historique de conversation: ", convo)
            
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
            
            # Process request
            await show_thinking_message()
            
            try:
                print(f"DEBUG: About to call Runner.run_streamed with last_agent type: {last_agent.name}")
                print(f"DEBUG: last_agent name: {last_agent.name}")
                print(f"DEBUG: convo type: {type(convo)}, length: {len(convo)}")
                
                result = Runner.run_streamed(last_agent, convo)
                print("DEBUG: Runner.run_streamed completed successfully")
                
                response_text = ""
                console.print("[dim]🔄 Traitement en cours...[/dim]")
                
                print("DEBUG: About to start streaming events")
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        response_text += event.data.delta
                print("DEBUG: Finished streaming events")
                
                # Clear processing message
                console.print("\033[1A\033[K", end="")
                
                # Display response
                if result.final_output:
                    print(f"DEBUG: result.last_agent.name: {result.last_agent.name}")
                    last_agent = result.last_agent
                    print(f"DEBUG: About to display response, last_agent type: {result.last_agent.name}")
                    display_response(result.last_agent.name, result.final_output) 
                else:
                    console.print(Panel("[red] Aucune réponse reçue[/red]", border_style="red"))
                
            except Exception as processing_error:
                print(f"DEBUG: Exception caught: {processing_error}")
                print(f"DEBUG: Exception type: {type(processing_error)}")
                console.print(show_error_panel(str(processing_error), "Erreur de traitement"))
                continue
                
            print("DEBUG: About to call result.to_input_list()")
            convo = result.to_input_list()
            print("DEBUG: result.to_input_list() completed")
            
            print(f"DEBUG: Updated last_agent: {last_agent.name}")
            console.print()
           
            
            
        except KeyboardInterrupt:
            console.print(show_interrupt_message())
            break
        except Exception as e:
            console.print(show_error_panel(str(e)))

if __name__ == "__main__":
    asyncio.run(main())