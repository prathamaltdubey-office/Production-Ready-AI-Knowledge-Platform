# API Documentation — Production-Ready AI Knowledge Platform

Base URL (local): `http://localhost:8000` All endpoints are versioned under `/api/v1/`, except the root health-style landing route.

## Authentication

Protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <API_TOKEN>
```

The token value is set via the `API_TOKEN` environment variable on the backend (see `.env`). Requests with a missing or invalid token receive `401 Unauthorized` with detail `"Invalid authentication token"`.

---

## Endpoints

### `GET /`

Landing route. Returns basic service metadata.

**Auth required:** No

**Response 200**

```json
{
  "message": "Customer Churn Prediction API",
  "version": "1.0.0"
}
```

---

### `GET /api/v1/health`

Health check for the service and its dependencies.

**Auth required:** No

**Response 200**

```json
{
  "status": "healthy",
  "ollama": "up",
  "faiss_index": "loaded"
}
```

- `status` is `"healthy"` only if both Ollama and the FAISS index are available; otherwise `"degraded"`.
- `ollama` is `"up"` or `"down"` based on a live check against the Ollama base URL.
- `faiss_index` is `"loaded"` or `"missing"` based on whether the index file exists on disk.

---

### `GET /api/v1/models`

Lists the ML models available for prediction.

**Auth required:** No

**Response 200**

```json
{
  "models": ["logistic_regression", "random_forest", "xgboost"]
}
```

---

### `GET /api/v1/models/{model_name}/versions`

Lists all registered versions of a specific model.

**Auth required:** Yes

**Path parameters**

| Name | Type | Description |
| --- | --- | --- |
| `model_name` | string | Name of the model to look up |

**Response 200**

```json
{
  "model_name": "random_forest",
  "versions": [1, 2, 3]
}
```

---

### `POST /api/v1/predict`

Predicts customer churn for a given customer profile.

**Auth required:** Yes

**Query parameters**

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `model_name` | string | — | Which model to use (e.g. `random_forest`) |
| `model_version` | string \| int | `"latest"` | Specific registered version, or `"latest"` |

**Request body** (`Customer`)

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.35,
  "TotalCharges": 845.5
}
```

| Field | Type | Constraints |
| --- | --- | --- |
| `gender` | `"Male"` \| `"Female"` | required |
| `SeniorCitizen` | `0` \| `1` | required |
| `Partner` | `"Yes"` \| `"No"` | required |
| `Dependents` | `"Yes"` \| `"No"` | required |
| `tenure` | int | `0–72` |
| `PhoneService` | `"Yes"` \| `"No"` | required |
| `MultipleLines` | `"Yes"` \| `"No"` \| `"No phone service"` | required |
| `InternetService` | `"DSL"` \| `"Fiber optic"` \| `"No"` | required |
| `OnlineSecurity` / `OnlineBackup` / `DeviceProtection` / `TechSupport` / `StreamingTV` / `StreamingMovies` | `"Yes"` \| `"No"` \| `"No internet service"` | required |
| `Contract` | `"Month-to-month"` \| `"One year"` \| `"Two year"` | required |
| `PaperlessBilling` | `"Yes"` \| `"No"` | required |
| `PaymentMethod` | `"Electronic check"` \| `"Mailed check"` \| `"Bank transfer (automatic)"` \| `"Credit card (automatic)"` | required |
| `MonthlyCharges` | float | `>= 0` |
| `TotalCharges` | float | `>= 0` |

**Response 200** (`PredictionResponse`)

```json
{
  "prediction": 1,
  "churn_probability": 0.734,
  "risk_level": "High",
  "model": "random_forest"
}
```

**Error responses**

- `401 Unauthorized` — missing/invalid token
- `4xx/500` — prediction failure (invalid model name/version, or an internal error); response includes an error `detail` message

---

### `POST /api/v1/chat`

Sends a message to the chatbot (RAG + agent pipeline) and returns a complete answer.

**Auth required:** Yes

**Request body** (`ChatRequest`)

```json
{
  "message": "What factors most influence customer churn?",
  "session_id": "default",
  "source": null
}
```

| Field | Type | Constraints |
| --- | --- | --- |
| `message` | string | 1–2000 characters, required |
| `session_id` | string | defaults to `"default"`; used to maintain conversation memory per session |
| `source` | string \| null | optional hint (e.g. restrict to prediction/RAG/document routing) |

**Response 200**

```json
{
  "answer": "Month-to-month contracts and high monthly charges are strongly associated with churn...",
  "citations": [
    { "source": "telco_churn_report.pdf", "snippet": "Customers on month-to-month contracts churn at higher rates..." }
  ]
}
```

*(Exact response shape depends on the RAG/agent implementation — confirm field names against `backend/api.py` if the frontend integration needs an exact match.)*

---

### `POST /api/v1/chat/stream`

Same as `/api/v1/chat`, but streams the response incrementally (Server-Sent Events or chunked response) for a more responsive chat UI.

**Auth required:** Yes

**Request body:** same as `/api/v1/chat`

**Response:** stream of text chunks as they are generated, terminated when generation completes.

---

### `POST /api/v1/upload`

Uploads a document (PDF, Markdown, or text) to be ingested into the RAG pipeline.

**Auth required:** Yes

**Request:** `multipart/form-data` with the file attached

**Response 200**

```json
{
  "filename": "telco_churn_report.pdf",
  "status": "ingested",
  "chunks_created": 42
}
```

---

### `GET /api/v1/documents`

Lists documents currently ingested into the RAG index.

**Auth required:** Yes

**Response 200**

```json
{
  "documents": ["telco_churn_report.pdf", "faq.md"]
}
```

---

### `GET /api/v1/documents/{filename}/content`

Retrieves the content (or metadata) of a specific ingested document.

**Auth required:** Yes

**Path parameters**

| Name | Type | Description |
| --- | --- | --- |
| `filename` | string | Name of the ingested document |

**Response 200**

```json
{
  "filename": "telco_churn_report.pdf",
  "content": "..."
}
```

**Error responses**

- `404 Not Found` — document does not exist

---

### `DELETE /api/v1/documents/{filename}`

Removes a document from the RAG index.

**Auth required:** Yes

**Path parameters**

| Name | Type | Description |
| --- | --- | --- |
| `filename` | string | Name of the document to remove |

**Response 200**

```json
{
  "filename": "telco_churn_report.pdf",
  "status": "deleted"
}
```

---

## Error Handling

All endpoints use consistent FastAPI `HTTPException` responses:

```json
{
  "detail": "Human-readable error message"
}
```

Common status codes:

| Code | Meaning |
| --- | --- |
| `400` | Invalid request (e.g. bad model name/version) |
| `401` | Missing or invalid auth token |
| `404` | Resource not found (e.g. unknown document) |
| `500` | Internal server error (logged via `logger.exception`) |

## Notes

- The exact response shape of `/api/v1/chat` and `/api/v1/chat/stream` should be verified against the current implementation in `backend/api.py`, since citation formatting may evolve as the frontend citation feature is completed.
- Interactive Swagger/OpenAPI docs are available at `http://localhost:8000/docs` when the backend is running — use this for live testing alongside this guide.