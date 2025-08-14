from agents import Agent
from output_config import UserProfile

def create_profiler_agent():
    """Create and configure the Profiler agent"""
    instructions = """
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
        
        Si tu reçois une demande d'un utilisateur et tu ne sais pas quoi répondre, et que la demande ne vient pas directement de l'agent trieur, alors tu transfères la demande à l'agent Trieur.

        """

    return Agent(
        name="Profiler",
        instructions=instructions,
        output_type=UserProfile,
        model="gpt-4o-mini",
    )