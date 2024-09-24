import discord
import asyncio
import requests
import random

from config.env import *
from config.persona import *
from classes.botstate import BotState

state = BotState(persona, API_MAX_CONTEXT_SIZE)
client = discord.Bot()

@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="you"))
  asyncio.create_task(check_messages())

# When the message is reacted with 🔁, the bot will regenerate the last message
async def rethink(message, bot_reply):
  global state
  
  def check(reaction, user):
    return user == message.author and str(reaction.emoji) == '🔁' and bot_reply.id == state.last_bot_message_id
  
  try:
    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
  except asyncio.TimeoutError:
    return
  else:
    await bot_reply.edit(content="*Thinking...*")

    state.context = state.context[:state.context.rfind("\n", 0, state.context.rfind("\n"))] + "\n"

    output = generate_output()
    while not output.strip():
      output = generate_output()
    filtered_output = output.replace(name + ":", "").strip()
    
    state.add_to_context(output)
    await bot_reply.edit(content=filtered_output)
    
    # Recur if reaction added again
    asyncio.create_task(rethink(message, bot_reply))

# Every incoming message is stored in a queue and processed one by one.
# This happens every 3 seconds, by default.
async def check_messages():
  global state
  while True:
    if state.message_queue and not state.thinking:
      state.thinking = True

      message = state.message_queue.pop(0)
      state.last_channel = message.channel
      filtered_message = remove_mentions(message.content).strip()
      state.add_to_context(f"{message.author.name}: {filtered_message}")

      async with message.channel.typing():
        output = generate_output()
        while not output.strip():
          output = generate_output()
        filtered_output = output.replace(name + ":", "").strip()

        state.add_to_context(output)
        bot_reply = None

        try:
          bot_reply = await message.channel.send(filtered_output, reference=message, mention_author=False)
          state.last_bot_message_id = bot_reply.id
        except Exception as e:
          print(e)

      state.thinking = False
      if bot_reply:
        asyncio.create_task(rethink(message, bot_reply))
    await asyncio.sleep(QUEUE_DELAY)

# Store incoming messages in the queue
@client.event
async def on_message(message):
  global state
  if message.author == client.user or USE_INTERACTION_WHITELIST and message.author.id not in INTERACTION_WHITELIST:
    return
  if client.user.mentioned_in(message):
    state.last_user_message_id = message.id
    state.message_queue.append(message)

# Remove mentions of the bot from the message, to avoid confusion for the bot
def remove_mentions(text):
  return text.replace(f"<@!{client.user.id}>", name).replace(f"<@{client.user.id}>", name)

def filter_output(response):
  lines = response.split("\n")
  filtered_response = ""
  found_name = False

  for line in lines:
    if line.startswith(name):
      found_name = True
      filtered_response += line.replace(name + ":", "").strip() + " "
    elif found_name:
      break

  return f"{name}: {filtered_response.strip()}"

# Generate a response using the API
def generate_output():
  data = {
    "model": API_MODEL,
    "prompt": persona + "\n" + state.context,
    "stream": False,
    "options": {
      "temperature": API_TEMPERATURE,
      "top_p": API_TOP_P,
      "frequency_penalty": API_FREQUENCY_PENALTY,
      "presence_penalty": API_PRESENCE_PENALTY
    }
  }

  response = requests.post(API_ENDPOINT + "api/generate", json=data)

  if response.status_code == 200:
    try:
      return filter_output(response.json().get('response', ''))
    except Exception as e:
      print(f"Error processing output: {e}")
      return "Error in generation."
  else:
    return f'Error: {response.status_code} - {response.text}'

if __name__ == "__main__":
  try:
    client.run(DISCORD_KEY)
  except Exception as e:
    print(f"Error running bot: {e}")
