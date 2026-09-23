const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const API_TOKEN = import.meta.env.VITE_API_TOKEN;

/**
 * Get or create a persistent session ID for this browser,
 * so chat memory stays isolated per user/session on the backend.
 */
const getSessionId = () => {
  let sessionId = localStorage.getItem("session-id");

  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session-id", sessionId);
  }

  return sessionId;
};

/**
 * Generic API request helper.
 */
const apiRequest = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,

    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_TOKEN}`,
      ...(options.headers || {}),
    },
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    // Response may not contain JSON.
  }

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      "API request failed.";

    throw new Error(errorMessage);
  }

  return data;
};

/**
 * Send a message to the chatbot.
 */
export const sendChatMessage = async (message, source = null) => {
  return apiRequest("/api/v1/chat", {
    method: "POST",

    body: JSON.stringify({
      message,
      session_id: getSessionId(),
      ...(source ? { source } : {}),
    }),
  });
};

/**
 * Predict customer churn.
 */
export const predictCustomer = async (
  customer,
  modelName = "random_forest"
) => {
  const query = new URLSearchParams({
    model_name: modelName,
  });

  return apiRequest(
    `/api/v1/predict?${query.toString()}`,
    {
      method: "POST",
      body: JSON.stringify(customer),
    }
  );
};

/**
 * Upload a document to the backend.
 *
 * Supported:
 * - PDF
 * - TXT
 * - Markdown
 */
export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/v1/upload`,
    {
      method: "POST",

      headers: {
        Authorization: `Bearer ${API_TOKEN}`,
      },

      body: formData,
    }
  );

  let data = null;

  try {
    data = await response.json();
  } catch {
    // Response may not contain JSON.
  }

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      "File upload failed.";

    throw new Error(errorMessage);
  }

  return data;
};

/**
 * Get all uploaded documents.
 */
export const getDocuments = async () => {
  return apiRequest("/api/v1/documents", {
    method: "GET",
  });
};

/**
 * Get the content of a single document for preview.
 */
export const getDocumentContent = async (filename) => {
  return apiRequest(
    `/api/v1/documents/${encodeURIComponent(filename)}/content`,
    { method: "GET" }
  );
};

/**
 * Delete a document.
 */
export const deleteDocument = async (filename) => {
  return apiRequest(
    `/api/v1/documents/${encodeURIComponent(filename)}`,
    { method: "DELETE" }
  );
};

/**
 * Send a message to the chatbot and receive the response as
 * a stream of text chunks, updating the UI progressively.
 */
export const sendChatMessageStream = async (
  message,
  source,
  onChunk
) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_TOKEN}`,
    },
    body: JSON.stringify({
      message,
      session_id: getSessionId(),
      ...(source ? { source } : {}),
    }),
  });

  if (!response.ok || !response.body) {
    throw new Error("Streaming request failed.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let fullText = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      break;
    }

    const chunkText = decoder.decode(value, { stream: true });
    fullText += chunkText;

    onChunk(fullText);
  }

  return fullText;
};