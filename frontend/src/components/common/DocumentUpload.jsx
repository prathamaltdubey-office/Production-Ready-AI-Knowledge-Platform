import { useEffect, useRef, useState } from "react";

import {
  getDocuments,
  uploadDocument,
  getDocumentContent,
  deleteDocument,
} from "../../services/api";

const MAX_FILE_SIZE = 10 * 1024 * 1024;

const ALLOWED_TYPES = [".pdf", ".txt", ".md"];

const DocumentUpload = ({ onNavigateToChat }) => {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState("");
  const [loadingDocuments, setLoadingDocuments] = useState(true);

  const [previewDoc, setPreviewDoc] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState("");

  const [deletingFilename, setDeletingFilename] = useState(null);

  // ------------------------------------------------------------
  // LOAD DOCUMENTS
  // ------------------------------------------------------------

  const loadDocuments = async () => {
    try {
      setLoadingDocuments(true);

      const response = await getDocuments();

      setDocuments(
        Array.isArray(response) ? response : response?.documents || []
      );
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setLoadingDocuments(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  // ------------------------------------------------------------
  // FILE VALIDATION
  // ------------------------------------------------------------

  const validateFile = (file) => {
    if (!file) {
      return "Please select a file.";
    }

    const extension = "." + file.name.split(".").pop().toLowerCase();

    if (!ALLOWED_TYPES.includes(extension)) {
      return "Only PDF, TXT, and Markdown files are supported.";
    }

    if (file.size > MAX_FILE_SIZE) {
      return "File size must be 10 MB or smaller.";
    }

    return "";
  };

  // ------------------------------------------------------------
  // SELECT FILE
  // ------------------------------------------------------------

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    setError("");
    setUploadResult(null);

    const validationError = validateFile(file);

    if (validationError) {
      setSelectedFile(null);
      setError(validationError);
      return;
    }

    setSelectedFile(file);
  };

  // ------------------------------------------------------------
  // UPLOAD
  // ------------------------------------------------------------

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    setUploading(true);
    setError("");
    setUploadResult(null);

    try {
      const result = await uploadDocument(selectedFile);

      setUploadResult(result);
      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      await loadDocuments();
    } catch (err) {
      console.error("Document upload failed:", err);
      setError(err.message || "Document upload failed.");
    } finally {
      setUploading(false);
    }
  };

  // ------------------------------------------------------------
  // PREVIEW
  // ------------------------------------------------------------

  const handlePreview = async (filename) => {
    setPreviewError("");
    setPreviewLoading(true);
    setPreviewDoc({ filename, content: "", truncated: false });

    try {
      const result = await getDocumentContent(filename);
      setPreviewDoc(result);
    } catch (err) {
      console.error("Failed to load preview:", err);
      setPreviewError(err.message || "Failed to load document preview.");
    } finally {
      setPreviewLoading(false);
    }
  };

  const closePreview = () => {
    setPreviewDoc(null);
    setPreviewError("");
  };

  // ------------------------------------------------------------
  // DELETE
  // ------------------------------------------------------------

  const handleDelete = async (filename, event) => {
    event.stopPropagation();

    const confirmed = window.confirm(
      `Delete "${filename}"? This cannot be undone.`
    );

    if (!confirmed) {
      return;
    }

    setDeletingFilename(filename);

    try {
      await deleteDocument(filename);
      await loadDocuments();

      if (previewDoc?.filename === filename) {
        closePreview();
      }
    } catch (err) {
      console.error("Delete failed:", err);
      setError(err.message || "Failed to delete document.");
    } finally {
      setDeletingFilename(null);
    }
  };

  // ------------------------------------------------------------
  // FORMAT FILE SIZE
  // ------------------------------------------------------------

  const formatFileSize = (bytes) => {
    if (!bytes) return "0 B";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <section className="glass document-upload-panel">
      {/* HEADER */}
      <div className="panel-header">
        <div className="panel-title-row">
          <div className="panel-icon prediction-icon">📄</div>
          <div>
            <h2>Document Knowledge Base</h2>
            <p>Upload documents for AI knowledge retrieval.</p>
          </div>
        </div>
      </div>

      <div className="document-upload-content">
        {/* UPLOAD AREA */}
        <div
          className="document-dropzone"
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="document-upload-icon">📄</div>
          <h3>{selectedFile ? selectedFile.name : "Choose a document"}</h3>
          <p>PDF, TXT or Markdown</p>
          <span>Maximum file size: 10 MB</span>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt,.md"
            onChange={handleFileChange}
            hidden
          />
        </div>

        {selectedFile && (
          <div className="selected-document">
            <div>
              <strong>{selectedFile.name}</strong>
              <span>{formatFileSize(selectedFile.size)}</span>
            </div>
            <button
              type="button"
              onClick={handleUpload}
              disabled={uploading}
              className="document-upload-button"
            >
              {uploading ? "Uploading..." : "Upload Document"}
            </button>
          </div>
        )}

        {error && <div className="document-error">{error}</div>}

        {uploadResult && (
          <div className="document-success">
            <strong>✓ Document uploaded successfully</strong>
            <div className="upload-result-grid">
              <div>
                <span>File</span>
                <strong>{uploadResult.filename}</strong>
              </div>
              <div>
                <span>Size</span>
                <strong>{formatFileSize(uploadResult.size_bytes)}</strong>
              </div>
              <div>
                <span>Documents Loaded</span>
                <strong>{uploadResult.documents_loaded}</strong>
              </div>
              <div>
                <span>Chunks Created</span>
                <strong>{uploadResult.chunks_created}</strong>
              </div>
            </div>
            <button
              type="button"
              onClick={onNavigateToChat}
              className="document-upload-button"
              style={{ marginTop: "12px" }}
            >
              Ask about this document →
            </button>
          </div>
        )}

        {/* DOCUMENT LIST */}
        <div className="documents-section">
          <div className="documents-section-header">
            <div>
              <h3>Uploaded Documents</h3>
              <p>Click a document to preview it.</p>
            </div>
            <button
              type="button"
              onClick={loadDocuments}
              disabled={loadingDocuments}
              className="documents-refresh-button"
            >
              {loadingDocuments ? "Loading..." : "Refresh"}
            </button>
          </div>

          {loadingDocuments ? (
            <div className="documents-empty">Loading documents...</div>
          ) : documents.length === 0 ? (
            <div className="documents-empty">No documents uploaded yet.</div>
          ) : (
            <div className="documents-list">
              {documents.map((document, index) => {
                const filename =
                  document.filename || document.name || `doc-${index}`;

                return (
                  <div
                    className="document-item"
                    key={filename}
                    onClick={() => handlePreview(filename)}
                    role="button"
                    tabIndex={0}
                  >
                    <div className="document-item-icon">📄</div>

                    <div className="document-item-info">
                      <strong>{filename}</strong>
                      {document.size_bytes && (
                        <span>{formatFileSize(document.size_bytes)}</span>
                      )}
                    </div>

                    <button
                      type="button"
                      className="document-delete-button"
                      onClick={(event) => handleDelete(filename, event)}
                      disabled={deletingFilename === filename}
                      title="Delete document"
                    >
                      {deletingFilename === filename ? "..." : "✕"}
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* PREVIEW MODAL */}
      {previewDoc && (
        <div className="document-preview-overlay" onClick={closePreview}>
          <div
            className="document-preview-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="document-preview-header">
              <strong>{previewDoc.filename}</strong>
              <button
                type="button"
                onClick={closePreview}
                className="document-preview-close"
              >
                ✕
              </button>
            </div>

            <div className="document-preview-body">
              {previewLoading ? (
                <p>Loading preview...</p>
              ) : previewError ? (
                <p className="document-error">{previewError}</p>
              ) : (
                <>
                  <pre>{previewDoc.content}</pre>
                  {previewDoc.truncated && (
                    <p className="document-preview-truncated">
                      Preview truncated to first 5,000 characters.
                    </p>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default DocumentUpload;