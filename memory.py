import os
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()
client = MemoryClient()

messages = [
    {"role": "user", "content": "Thinking of making a sandwich. What do you recommend?"},
    {"role": "assistant", "content": "How about adding some cheese for extra flavor?"},
    {"role": "user", "content": "Actually, I don't like cheese."},
    {"role": "assistant", "content": "I'll remember that you don't like cheese for future recommendations."}
]
client.add(messages, user_id="alex")
print(client)