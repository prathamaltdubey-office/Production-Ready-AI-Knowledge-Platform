import ChatMessage from "./ChatMessage";

const MessageList = ({
  messages,
  loading,
}) => {
  return (
    <div className="messages">
      {messages.map((message, index) => (
        <ChatMessage
          key={`${message.role}-${index}`}
          message={message}
        />
      ))}

      {loading && (
        <div className="message assistant-message">
          <div className="message-avatar">
            AI
          </div>

          <div className="message-body">
            <div className="message-label">
              AI Assistant
            </div>

            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList;