import os
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.table import Table
from rich.align import Align
from rich.box import ROUNDED, DOUBLE_EDGE, MINIMAL_HEAVY_HEAD
from rich.tree import Tree
from rich.rule import Rule
from rich.layout import Layout

console = Console()

def create_header():
    """Create a beautiful header with gradient effect"""
    header_text = Text()
    header_text.append("", style="bold blue")
    header_text.append("Pete le", style="bold magenta")
    header_text.append(" Psy", style="bold cyan")
    header_text.append("", style="bold yellow")
    
    return Panel(
        Align.center(header_text),
        subtitle="[dim italic]Découvrez votre personnalité avec l'IA[/dim italic]",
        border_style="blue",
        box=DOUBLE_EDGE,
        padding=(1, 2)
    )

def create_agents_info():
    """Display available agents information"""
    tree = Tree("🤖 [bold blue]Agents Disponibles[/bold blue]")
    
    caracteriologue_branch = tree.add("🧑‍🔬 [bold green]Caractériologue[/bold green]")
    caracteriologue_branch.add("[dim]• Analyse votre caractère[/dim]")
    caracteriologue_branch.add("[dim]• Connais les travaux théoriques de la caractérologie[/dim]")
    
    interrogateur_branch = tree.add("❓ [bold yellow]Interrogateur[/bold yellow]")
    interrogateur_branch.add("[dim]• Pose des questions ciblées[/dim]")
    interrogateur_branch.add("[dim]• Permet de connaitre son propre caractère[/dim]")
    
    trieur_branch = tree.add("🎯 [bold magenta]Trieur[/bold magenta]")
    trieur_branch.add("[dim]• Détermine l'agent optimal[/dim]")
    trieur_branch.add("[dim]• Route intelligemment vos demandes[/dim]")
    
    return Panel(tree, border_style="dim", padding=(0, 1))

def create_commands_table():
    """Create a helpful commands table"""
    table = Table(show_header=True, header_style="bold magenta", box=MINIMAL_HEAVY_HEAD)
    table.add_column("Commande", style="cyan", width=15)
    table.add_column("Description", style="white")
    table.add_column("Exemple", style="dim")
    
    table.add_row("quit / exit / q", "Quitter l'application", "quit")
    table.add_row("clear", "Effacer l'écran", "clear")
    table.add_row("help", "Afficher cette aide", "help")
    table.add_row("agents", "Voir les agents disponibles", "agents")
    
    return Panel(
        table,
        title="[bold blue]📋 Commandes Utiles[/bold blue]",
        border_style="blue",
        padding=(1, 1)
    )

def create_status_panel(status_text, style="bold green"):
    """Create a status panel with animation"""
    return Panel(
        Align.center(f"[{style}]{status_text}[/{style}]"),
        border_style=style.split()[1] if " " in style else style,
        padding=(0, 2)
    )

def display_response(agent_name, response_text, response_type="response"):
    """Display agent response with beautiful formatting"""
    # Choose colors based on agent
    agent_colors = {
        "Caractériologue": ("green", "🧑‍🔬"),
        "Interrogateur": ("yellow", "❓"),
        "Trieur": ("magenta", "🎯"),
        "default": ("blue", "🤖")
    }
    
    color, emoji = agent_colors.get(agent_name, agent_colors["default"])
    
    # Display response in the same format as user input but keep markdown, centered
    console.print(f"[bold {color}]{agent_name}[/bold {color}]")
    console.print(Markdown(response_text))
    console.print()

def clear_screen():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Display help information"""
    help_content = """
## 🎯 Comment utiliser ce système

**Pour commencer :**
- Posez simplement une question sur votre personnalité
- Le système choisira automatiquement le bon agent pour vous

**Exemples de questions :**
- "Peux-tu analyser mon caractère ?"
- "Quelles questions peux-tu me poser ?"
- "Comment fonctionne la caractérologie ?"

**Navigation :**
- Utilisez les commandes listées ci-dessus
- L'historique de conversation est automatiquement conservé
    """
    
    console.print(Panel(
        Markdown(help_content),
        title="[bold cyan]📚 Guide d'Utilisation[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))

def show_goodbye_message():
    """Display goodbye message"""
    return Panel(
        Align.center("👋 [bold yellow]Merci d'avoir utilisé le système de caractérologie![/bold yellow]\n[dim]À bientôt pour découvrir encore plus sur votre personnalité![/dim]"),
        border_style="yellow",
        box=DOUBLE_EDGE,
        padding=(1, 2)
    )

def show_error_panel(error_message, title="Erreur"):
    """Display error panel"""
    return Panel(
        f"[bold red]Erreur technique:[/bold red]\n[dim]{error_message}[/dim]\n\n[yellow]",
        title=f"[bold red]{title}[/bold red]",
        border_style="red",
        padding=(1, 2)
    )

def show_interrupt_message():
    """Display keyboard interrupt message"""
    return Panel(
        Align.center("\n[yellow]Interruption détectée - Au revoir![/yellow]"),
        border_style="yellow"
    )