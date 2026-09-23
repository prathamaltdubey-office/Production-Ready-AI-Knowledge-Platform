import { useEffect, useState } from "react";
import { getDocuments, sendChatMessageStream } from "../services/api";

const STORAGE_KEY = "customer-churn-chat-history";

const createInitialMessage = () => ({
  role: "assistant",
  content:
    "Hello! I'm your Customer Churn AI Assistant. Ask me about customer churn, the ML project, or provide customer information for a churn prediction.",
});

const createConversation = () => ({
  id: crypto.randomUUID(),
  title: "New conversation",
  messages: [createInitialMessage()],
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
});

const loadConversations = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);

    if (!stored) {
      return [createConversation()];
    }

    const conversations = JSON.parse(stored);

    if (!Array.isArray(conversations) || conversations.length === 0) {
      return [createConversation()];
    }

    return conversations;
  } catch {
    return [createConversation()];
  }
};

const useChat = () => {
  const [conversations, setConversations] = useState(
    loadConversations
  );

  const [activeConversationId, setActiveConversationId] =
    useState(() => {
      const stored = loadConversations();
      return stored[0].id;
    });

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------
  // DOCUMENT SCOPE (chat with all documents, or one specific one)
  // ------------------------------------------------------------

  const [availableDocuments, setAvailableDocuments] = useState([]);
  const [selectedSource, setSelectedSource] = useState("");

  useEffect(() => {
    const loadDocs = async () => {
      try {
        const response = await getDocuments();

        const documents = Array.isArray(response)
          ? response
          : response?.documents || [];

        setAvailableDocuments(documents);
      } catch (err) {
        console.error("Failed to load documents for chat scope:", err);
      }
    };

    loadDocs();
  }, []);

  const activeConversation =
    conversations.find(
      (conversation) =>
        conversation.id === activeConversationId
    ) || conversations[0];

  const messages = activeConversation?.messages || [];

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(conversations)
    );
  }, [conversations]);

  const updateConversation = (conversationId, updater) => {
    setConversations((previousConversations) =>
      previousConversations.map((conversation) => {
        if (conversation.id !== conversationId) {
          return conversation;
        }

        return {
          ...updater(conversation),
          updatedAt: new Date().toISOString(),
        };
      })
    );
  };

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    const conversationId = activeConversationId;

    updateConversation(conversationId, (conversation) => {
      const isFirstUserMessage =
        conversation.messages.filter(
          (item) => item.role === "user"
        ).length === 0;

      return {
        ...conversation,
        title: isFirstUserMessage
          ? message.slice(0, 45)
          : conversation.title,
        messages: [
          ...conversation.messages,
          {
            role: "user",
            content: message,
          },
        ],
      };
    });

    setInput("");
    setLoading(true);

    try {
      // Add an empty assistant message first, which we'll fill in
      // progressively as chunks arrive.
      updateConversation(conversationId, (conversation) => ({
        ...conversation,
        messages: [
          ...conversation.messages,
          { role: "assistant", content: "" },
        ],
      }));

      await sendChatMessageStream(
        message,
        selectedSource || null,
        (partialText) => {
          updateConversation(conversationId, (conversation) => {
            const messages = [...conversation.messages];
            messages[messages.length - 1] = {
              role: "assistant",
              content: partialText,
            };
            return { ...conversation, messages };
          });
        }
      );
    } catch (error) {
      updateConversation(conversationId, (conversation) => ({
        ...conversation,
        messages: [
          ...conversation.messages,
          {
            role: "assistant",
            content:
              error.message ||
              "Sorry, something went wrong while contacting the AI service.",
          },
        ],
      }));
    } finally {
      setLoading(false);
    }
  };

  const createNewConversation = () => {
    const conversation = createConversation();

    setConversations((previousConversations) => [
      conversation,
      ...previousConversations,
    ]);

    setActiveConversationId(conversation.id);
    setInput("");
  };

  const selectConversation = (conversationId) => {
    if (loading) {
      return;
    }

    setActiveConversationId(conversationId);
    setInput("");
  };

  const deleteConversation = (conversationId) => {
    if (loading) {
      return;
    }

    setConversations((previousConversations) => {
      const remaining = previousConversations.filter(
        (conversation) =>
          conversation.id !== conversationId
      );

      if (remaining.length === 0) {
        const newConversation = createConversation();

        setActiveConversationId(newConversation.id);

        return [newConversation];
      }

      if (conversationId === activeConversationId) {
        setActiveConversationId(remaining[0].id);
      }

      return remaining;
    });
  };

  return {
    messages,
    input,
    setInput,
    loading,
    sendMessage,

    conversations,
    activeConversationId,
    createNewConversation,
    selectConversation,
    deleteConversation,

    availableDocuments,
    selectedSource,
    setSelectedSource,
  };
};

export default useChat;
