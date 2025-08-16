from agents import Agent, Runner, function_tool
from mem0 import MemoryClient
from dotenv import load_dotenv
from user_context import current_user

load_dotenv()

# Initialize memory client
mem0 = MemoryClient()
print("[DEBUG] Memory client initialized:", type(mem0))

# Define memory tools for the agent
@function_tool
def search_memory(query: str, user_id: str = None) -> str:
    """Search through past conversations and memories"""
    # Always use global context, ignore passed user_id
    passed_user_id = user_id
    user_id = current_user.get_user_id()
    
    if passed_user_id and passed_user_id != user_id:
        print(f"[DEBUG] search_memory ignoring passed user_id '{passed_user_id}', using global user_id: {user_id}")
    else:
        print(f"[DEBUG] search_memory using global user_id: {user_id}")
    
    print(f"[DEBUG] search_memory called with query='{query}', final user_id='{user_id}'")
    
    if user_id is None:
        return "Error: No user ID available for memory search."
    
    try:
        #memories = mem0.search(query, user_id=user_id, limit=3, version="v2")
        memories = mem0.search(
            query=query,
            version="v2",
            filters={
                "OR": [
                    {"user_id": user_id},
                ]
            }
        )
        
        print(f"[DEBUG] search_memory result type: {type(memories)}")
        print(f"[DEBUG] search_memory result: {memories}")
        
        # Handle both list format and dict format
        if isinstance(memories, list) and memories:
            # Direct list of memory objects
            result = "\n".join([f"- {mem['memory']}" for mem in memories])
            print(f"[DEBUG] search_memory returning: {result}")
            return result
        elif isinstance(memories, dict) and memories.get('results'):
            # Dict with 'results' key
            result = "\n".join([f"- {mem['memory']}" for mem in memories['results']])
            print(f"[DEBUG] search_memory returning: {result}")
            return result
        else:
            print("[DEBUG] search_memory: No results found")
            return "No relevant memories found."
    except Exception as e:
        print(f"[DEBUG] search_memory ERROR: {e}")
        return f"Error searching memories: {e}"

@function_tool
def save_memory(content: str, user_id: str = None) -> str:
    """Save important information to memory"""
    # Always use global context, ignore passed user_id
    passed_user_id = user_id
    user_id = current_user.get_user_id()
    
    if passed_user_id and passed_user_id != user_id:
        print(f"[DEBUG] save_memory ignoring passed user_id '{passed_user_id}', using global user_id: {user_id}")
    else:
        print(f"[DEBUG] save_memory using global user_id: {user_id}")
    
    print(f"[DEBUG] save_memory called with content='{content}', final user_id='{user_id}'")
    
    if user_id is None:
        return "Error: No user ID available for saving memory."
    
    try:
        result = mem0.add([{"role": "user", "content": content}], user_id=user_id, version="v2")
        print(f"[DEBUG] save_memory add result: {result}")
        return "Information saved to memory."
    except Exception as e:
        print(f"[DEBUG] save_memory ERROR: {e}")
        return f"Error saving memory: {e}"




