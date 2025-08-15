from agent.trieur import create_trieur_agent
from agent.caracteriologue import create_caracteriologue_agent
from agent.interrogateur import create_interrogateur_agent
from agent.profiler import create_profiler_agent

def create_agents():
    """Create and configure all agents"""
    trieur_agent = create_trieur_agent()
    caracteriologue_agent = create_caracteriologue_agent()
    interrogateur_agent = create_interrogateur_agent()
    profiler_agent = create_profiler_agent()

    #caracteriologue_agent.handoffs = [trieur_agent]
    interrogateur_agent.handoffs = [caracteriologue_agent]
    trieur_agent.handoffs = [caracteriologue_agent, interrogateur_agent]
    #profiler_agent.handoffs = [trieur_agent]  


    return {
        "caracteriologue": caracteriologue_agent,
        "interrogateur": interrogateur_agent,
        "trieur": trieur_agent,
        "profiler": profiler_agent
    }

def get_agent_by_name(agents_dict, name):
    """Get agent by name with fallback"""
    return agents_dict.get(name.lower(), agents_dict["trieur"])