# Ollama Discord Bot

This project is a `discord.py`-based bot that integrates with the Ollama API, enabling an AI-powered companion for your Discord server. The bot can hold dynamic conversations and adapt its responses based on a context system, while also allowing you to define its personality traits and characteristics.

## Features

- **Ollama API Integration**: Generates conversational responses using Ollama’s API.
- **Context System**: Maintains a conversation history, providing more coherent and relevant responses.
- **Customizable Personality**: Easily give the AI different personalities through the persona system.
- **Message Queue**: Manages incoming messages in a queue to process them one at a time, preventing overload.
- **Reaction-based Rethinking**: Allows users to react to a bot message with 🔁 to regenerate the last response.

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed and the following dependencies:

- `discord.py==2.4.0`
- `requests==2.32.3`

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

## Setup
Clone the repository:
```bash
git clone https://github.com/StormTersteeg/OllamaDiscordAI.git
```

### Configure environment variables:

Update the env.py file with the following:
- `DISCORD_KEY`: Your Discord bot token.
- `API_ENDPOINT`: The endpoint URL for your Ollama API.
- `API_MODEL`: The AI model to be used for generating responses (e.g., LLama-3.1-8b-q5-k-m).

Customize the persona:
Modify `persona.py` to adjust the personality and tone of your bot. The file defines the bot's character, its name, and how it responds to user inputs.

### Run the bot
```bash
python bot.py
```

## Key Configuration Options
- `API_MAX_CONTEXT_SIZE`: Maximum context size for API interactions. This controls how much conversation history is maintained.
- `API_TEMPERATURE`: Controls the randomness of the responses (higher values make responses more random).
- `USE_INTERACTION_WHITELIST`: Set to True if you want to restrict bot interactions to a specific list of users.
- `QUEUE_DELAY`: Sets the delay between processing each message in the queue (default is 3 seconds).

## Bot Features
- `Message Queue`: The bot processes incoming messages every 3 seconds, ensuring only one message is processed at a time.
- `Context Management`: The bot keeps track of conversation history in context.txt, allowing it to maintain context across multiple messages.
- `Rethink with Reactions`: Users can react to the bot’s last message with 🔁, prompting the bot to generate a new response.

## File Structure
```bash
/ollama-discord-bot
│
├── bot.py                 # Main bot logic
├── classes/
│   └── botstate.py         # Bot state management, message queue, context handling
├── env.py                  # Environment variables, API settings
├── persona.py              # Persona configuration for the bot's character and behavior
├── requirements.txt        # Required Python dependencies
└── context.txt             # Stores conversation history for context
```

## Example Usage
Once the bot is running, simply mention the bot in a channel like:<br>
`@Blue Tell me a joke!`

The bot will reply based on its persona and context:<br>
`Blue: Haha, okay! Why don’t skeletons fight each other? They don’t have the guts! 😎`

<hr><br>
Happy chatting with your AI-powered Discord companion!
