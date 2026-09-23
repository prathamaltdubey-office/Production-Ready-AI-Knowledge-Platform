from langchain_core.chat_history import InMemoryChatMessageHistory


class ConversationMemory:
    """Store conversation messages for the current chatbot session."""

    def __init__(self):
        self.history = InMemoryChatMessageHistory()

    def add_user_message(self, message: str) -> None:
        """Store a user message."""
        self.history.add_user_message(message)

    def add_ai_message(self, message: str) -> None:
        """Store an AI response."""
        self.history.add_ai_message(message)

    def get_messages(self):
        """Return all stored conversation messages."""
        return self.history.messages

    def clear(self) -> None:
        """Clear the conversation history."""
        self.history.clear()
