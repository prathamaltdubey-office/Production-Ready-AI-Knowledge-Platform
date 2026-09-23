import useChat from "../../hooks/useChat";

import MessageList from "./MessageList";
import ChatInput from "./ChatInput";

const ChatPanel = () => {
  const {
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
  } = useChat();

  return (
    <section className="chat-section glass">
      <div className="chat-layout">
        {/* CHAT HISTORY */}
        <aside className="chat-history">
          <div className="chat-history-header">
            <div>
              <h3>Chat History</h3>
              <p>Recent conversations</p>
            </div>

            <button
              type="button"
              className="new-chat-button"
              onClick={createNewConversation}
              disabled={loading}
              title="New conversation"
            >
              +
            </button>
          </div>

          <div className="chat-history-list">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`chat-history-item ${
                  activeConversationId === conversation.id
                    ? "active"
                    : ""
                }`}
              >
                <button
                  type="button"
                  className="chat-history-select"
                  onClick={() =>
                    selectConversation(conversation.id)
                  }
                  disabled={loading}
                >
                  <span className="history-icon">✦</span>
                  <span className="history-title">
                    {conversation.title}
                  </span>
                </button>

                <button
                  type="button"
                  className="history-delete"
                  onClick={() =>
                    deleteConversation(conversation.id)
                  }
                  disabled={loading}
                  title="Delete conversation"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </aside>

        {/* CURRENT CHAT */}
        <div className="chat-main">
          <div className="panel-header">
            <div className="panel-title-row">
              <div className="panel-icon chat-icon">✦</div>

              <div>
                <h2>AI Chat Assistant</h2>
                <p>
                  Ask questions about customer churn,
                  the ML project, or predictions.
                </p>
              </div>
            </div>

            <div className="mini-status">
              <span></span>
              Online
            </div>
          </div>

          {/* DOCUMENT SCOPE SELECTOR */}
          <div className="chat-scope-row">
            <label htmlFor="chat-scope-select">
              Chat with:
            </label>

            <select
              id="chat-scope-select"
              className="chat-scope-select"
              value={selectedSource}
              onChange={(event) =>
                setSelectedSource(event.target.value)
              }
              disabled={loading}
            >
              <option value="">All Documents</option>

              {availableDocuments.map((document) => {
                const filename =
                  document.filename || document.name;

                return (
                  <option key={filename} value={filename}>
                    {filename}
                  </option>
                );
              })}
            </select>
          </div>

          <div className="chat-container">
            <MessageList
              messages={messages}
              loading={loading}
            />

            <ChatInput
              input={input}
              setInput={setInput}
              loading={loading}
              sendMessage={sendMessage}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;