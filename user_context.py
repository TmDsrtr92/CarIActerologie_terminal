# Global user context for sharing user_id across the application
# This is a simple solution to pass user_id to function tools
from debug_utils import debug_print

class UserContext:
    """Global context to store current user information"""
    def __init__(self):
        self._user_id = None
    
    def set_user_id(self, user_id):
        """Set the current user ID"""
        self._user_id = user_id
        debug_print(f"[DEBUG] Global user_id set to: {user_id}")
    
    def get_user_id(self):
        """Get the current user ID"""
        if self._user_id is None:
            debug_print("[DEBUG] Warning: No user_id set in global context")
        return self._user_id
    
    def clear(self):
        """Clear the current user context"""
        debug_print(f"[DEBUG] Clearing global user_id: {self._user_id}")
        self._user_id = None

# Global instance
current_user = UserContext()