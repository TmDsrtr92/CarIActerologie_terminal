from agents import Agent, Runner
from pydantic import BaseModel, Field
import asyncio
from dotenv import load_dotenv
from typing import Literal
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

load_dotenv()
console = Console()

class UserProfile(BaseModel):
    caractere: Literal["Nerveux", "Sentimental", "Colérique", "Passionné", "Sanguin", "Flegmatique", "Amorphique", "Apathique"] = Field(description="Type caractérologique de l'utilisateur")
    emotivite: Literal["Oui", "Non"] = Field(description="Si l'utilisateur est émotif ou non")
    activite: Literal["Oui", "Non"] = Field(description="Si l'utilisateur est actif ou non")
    retentissement: Literal["Primaire", "Secondaire"] = Field(description="Si l'utilisateur a un retentissement primaire ou secondaire")

def display_header():
    """Display fancy header"""
    header = Text("🧠 ANALYSE CARACTÉROLOGIQUE", style="bold magenta", justify="center")
    console.print(Panel(header, border_style="magenta", padding=(1, 2)))
    console.print()

def display_conversation_sample(sample_convo):
    """Display conversation sample in a nice format"""
    console.print("📝 [bold cyan]Échantillon de conversation analysé:[/bold cyan]")
    
    for i, msg in enumerate(sample_convo, 1):
        if msg["role"] == "user":
            console.print(f"[bold green]👤 Utilisateur:[/bold green] {msg['content']}")
        else:
            console.print(f"[dim]🤖 Assistant:[/dim] [dim]{msg['content']}[/dim]")
    console.print()

def create_profile_table(profile):
    """Create a fancy table for the profile results"""
    table = Table(title="🎯 Profil Caractérologique Détecté", border_style="blue")
    
    table.add_column("Dimension", style="cyan", no_wrap=True)
    table.add_column("Résultat", style="magenta")
    table.add_column("Description", style="dim")
    
    # Character type with emoji
    char_emoji = {
        "Nerveux": "⚡", "Sentimental": "💝", "Colérique": "🔥", "Passionné": "❤️‍🔥",
        "Sanguin": "☀️", "Flegmatique": "🧘", "Amorphique": "🌫️", "Apathique": "😴"
    }
    
    table.add_row(
        "Caractère",
        f"{char_emoji.get(profile.caractere, '🔍')} {profile.caractere}",
        "Type caractérologique principal"
    )
    
    # Emotivity
    emotivity_style = "green" if profile.emotivite == "Oui" else "yellow"
    emotivity_emoji = "💭" if profile.emotivite == "Oui" else "🧊"
    table.add_row(
        "Émotivité",
        f"[{emotivity_style}]{emotivity_emoji} {profile.emotivite}[/{emotivity_style}]",
        "Réactivité émotionnelle"
    )
    
    # Activity
    activity_style = "green" if profile.activite == "Oui" else "yellow"
    activity_emoji = "🏃" if profile.activite == "Oui" else "🪑"
    table.add_row(
        "Activité",
        f"[{activity_style}]{activity_emoji} {profile.activite}[/{activity_style}]",
        "Tendance à l'action"
    )
    
    # Retentissement
    ret_style = "blue" if profile.retentissement == "Primaire" else "purple"
    ret_emoji = "⚡" if profile.retentissement == "Primaire" else "🔄"
    table.add_row(
        "Retentissement",
        f"[{ret_style}]{ret_emoji} {profile.retentissement}[/{ret_style}]",
        "Durée des impressions"
    )
    
    return table

async def main():
    # Display header
    display_header()
    
    # Sample conversation history
    sample_convo = [
        {"content": "Bonjour, je m'appelle Marie", "role": "user"},
        {"content": "Bonjour Marie ! Comment allez-vous aujourd'hui ?", "role": "assistant"},
        {"content": "Je vais bien merci. Je suis quelqu'un qui réagit très vite aux événements, parfois trop vite d'ailleurs", "role": "user"},
        {"content": "Je comprends. Pouvez-vous me parler un peu plus de vous ?", "role": "assistant"},
        {"content": "J'aime bouger, faire du sport, voyager. Je n'aime pas rester inactive. Quand quelque chose me plaît, j'y pense longtemps après", "role": "user"},
        {"content": "C'est intéressant. Comment réagissez-vous face aux imprévus ?", "role": "assistant"},
        {"content": "Je me mets souvent en colère rapidement, mais ça passe vite aussi. Je prends les décisions rapidement", "role": "user"}
    ]
    
    # Display conversation sample
    display_conversation_sample(sample_convo)
    
    # Create agent
    profiler_agent = Agent(
        name="Profiler",
        instructions="""
        Analysez l'historique de conversation fourni pour déterminer le profil caractérologique de l'utilisateur selon la caractérologie de Heymans-Le Senne.

        Déterminez :
        1. ÉMOTIVITÉ : "Oui" si la personne réagit facilement aux événements, se laisse émouvoir, "Non" si elle reste calme et maîtresse d'elle-même
        2. ACTIVITÉ : "Oui" si la personne aime l'action, le mouvement, entreprendre, "Non" si elle préfère la réflexion à l'action
        3. RETENTISSEMENT : "Primaire" si les impressions s'effacent rapidement, "Secondaire" si elles persistent et influencent durablement

        Les 8 caractères possibles :
        - Nerveux (É+, A-, P) : émotif, non-actif, primaire
        - Sentimental (É+, A-, S) : émotif, non-actif, secondaire  
        - Colérique (É+, A+, P) : émotif, actif, primaire
        - Passionné (É+, A+, S) : émotif, actif, secondaire
        - Sanguin (É-, A+, P) : non-émotif, actif, primaire
        - Flegmatique (É-, A+, S) : non-émotif, actif, secondaire
        - Amorphique (É-, A-, P) : non-émotif, non-actif, primaire
        - Apathique (É-, A-, S) : non-émotif, non-actif, secondaire

        Basez-vous uniquement sur les éléments présents dans la conversation.
        """,
        output_type=UserProfile,
    )
    
    # Show processing with spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("🔬 Analyse du profil en cours...", total=None)
        result = await Runner.run(profiler_agent, sample_convo)
    
    profile = result.final_output
    
    # Display results in fancy table
    console.print(create_profile_table(profile))
    
    # Success message
    console.print()
    console.print(Panel(
        "✅ [bold green]Analyse terminée avec succès![/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

if __name__ == "__main__":
    asyncio.run(main())



