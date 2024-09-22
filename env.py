USE_INTERACTION_WHITELIST = False            # Whether to use the interaction whitelist.
INTERACTION_WHITELIST = []                   # List of user IDs that can interact with the bot.
QUEUE_DELAY = 3                              # Delay between processing messages.

API_ENDPOINT = "http://localhost:10002/"     # URL of the Ollama API.
API_MODEL = "LLama-3.1-8b-q5-k-m"            # Model to use for generating responses.
API_MAX_CONTEXT_SIZE = 30000                 # Maximum context size for the API. 8192 maximum token length, approx 32768 characters.
API_TEMPERATURE = 0.8                        # Temperature for response generation.
API_TOP_P = 0.9                              # Top-p for response generation.
API_FREQUENCY_PENALTY = 0.5                  # Frequency penalty for response generation.
API_PRESENCE_PENALTY = 0.5                   # Presence penalty for response generation.

DISCORD_KEY = "your_discord_key_here"