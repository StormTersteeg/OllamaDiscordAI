class BotState:
  def __init__(self, persona, max_context_size):
    self.message_queue = []
    self.thinking = False
    self.last_channel = None
    self.last_user_message_id = None
    self.last_bot_message_id = None
    self.context = self.load_context()
    self.context_size = max_context_size - len(persona)

  def load_context(self):
    with open("context.txt", "r", encoding="utf-8") as f:
      return f.read()

  def save_context(self):
    with open("context.txt", "w", encoding="utf-8") as f:
      f.write(self.context)

  def add_to_context(self, prompt):
    self.context += prompt + "\n"
    self.context = self.context[-self.context_size:]
    self.save_context()