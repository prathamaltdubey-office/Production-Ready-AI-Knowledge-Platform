const ChatInput = ({
  input,
  setInput,
  loading,
  sendMessage,
}) => {
  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="input-area">
      <input
        type="text"
        placeholder="Ask something about customer churn..."
        value={input}
        disabled={loading}
        onChange={(event) =>
          setInput(event.target.value)
        }
        onKeyDown={handleKeyDown}
      />

      <button
        className="send-button"
        onClick={sendMessage}
        disabled={
          loading || !input.trim()
        }
      >
        {loading ? (
          <span className="button-spinner"></span>
        ) : (
          "Send"
        )}
      </button>
    </div>
  );
};

export default ChatInput;