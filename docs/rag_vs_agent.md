# Standard RAG vs Agentic AI

## 1. Overview

The Enterprise Knowledge Assistant contains two approaches for answering
questions:

1. Standard Retrieval-Augmented Generation (RAG)
2. Agentic AI

Both approaches can answer questions using enterprise documents, but the
agentic approach can additionally select and execute different tools based
on the user's request.

---

## 2. Standard RAG Workflow

The standard RAG pipeline follows this workflow:

User Query
    |
    v
Query Embedding
    |
    v
Vector Search
    |
    v
Relevant Documents
    |
    v
Prompt + Retrieved Context
    |
    v
LLM
    |
    v
Final Answer

The standard RAG system is primarily designed to answer questions using
information contained in the enterprise document collection.

---

## 3. Agentic AI Workflow

The agentic system introduces an agent that can select tools dynamically.

User Query
    |
    v
Agent
    |
    +----> Calculator
    |
    +----> Wikipedia
    |
    +----> DuckDuckGo Search
    |
    +----> Python REPL
    |
    +----> File Reader
    |
    +----> Document Retriever
    |
    v
Tool Results
    |
    v
Agent
    |
    v
Final Answer

The agent can use one or multiple tools depending on the question.

---

## 4. Main Difference

The main difference is that standard RAG retrieves information and provides
that information to an LLM, while an agent can decide what action should be
performed.

Standard RAG:

    Query
      |
      v
  Retrieval
      |
      v
    LLM
      |
      v
   Answer

Agentic AI:

    Query
      |
      v
    Agent
      |
      +--> Tool 1
      |
      +--> Tool 2
      |
      +--> Tool 3
      |
      v
    Results
      |
      v
   Final Answer

---

## 5. Comparison Test

The two approaches were tested using three questions.

### Question 1

What are the key features of the SmartHome Hub?

### Standard RAG

The RAG pipeline successfully retrieved the relevant SmartHome Hub document
information and generated an answer containing:

- Universal Compatibility
- AI-Powered Assistant
- Enhanced Security

### Agentic AI

The agent selected the Document Retriever tool and generated an answer
containing the same key features.

Result:

Both systems successfully answered the question.

---

## 6. Question 2

What is SmartTech Co.'s market share?

### Standard RAG

The RAG pipeline retrieved the competitor analysis information and returned:

SmartTech Co. market share = 35%

### Agentic AI

The agent selected the Document Retriever tool and returned:

SmartTech Co. market share = 35%

Result:

Both systems successfully answered the question.

---

## 7. Question 3

What is 125 multiplied by 48?

### Standard RAG

The standard RAG system could not answer the question because the
calculation was not contained in the enterprise documents.

The system correctly reported that the information was not available in the
provided documents.

### Agentic AI

The agent identified this as a mathematical operation and selected the
Calculator tool.

Calculation:

125 × 48 = 6000

Result:

The agent successfully answered the question.

---

## 8. Comparison Table

| Capability | Standard RAG | Agentic AI |
|---|---|---|
| Enterprise document questions | Yes | Yes |
| Semantic document retrieval | Yes | Yes |
| Grounded responses | Yes | Yes |
| Mathematical calculations | Document dependent | Calculator tool |
| Web search | No | DuckDuckGo tool |
| Wikipedia search | No | Wikipedia tool |
| Python execution | No | Python REPL |
| Local file reading | No | File Reader |
| Multiple tools in one request | No | Yes |
| Dynamic tool selection | No | Yes |
| Multi-step execution | Limited | Yes |
| Error recovery | Basic | Tool-aware recovery |
| Conversational memory | Limited | Implemented |

---

## 9. Multi-Step Agent Example

The agent was tested with the following question:

"What is SmartTech Co.'s market share according to the SmartHome Hub
document, and calculate what 35% of the projected $135.3 billion smart home
market would be?"

The agent performed multiple operations.

### Step 1 — Document Retrieval

The Document Retriever found:

SmartTech Co. market share = 35%

### Step 2 — Calculation

The Calculator performed:

0.35 × 135,300,000,000

Result:

47,355,000,000

### Step 3 — Final Response

The agent combined the retrieved information and calculation into a final
answer:

SmartTech Co.'s market share is 35%.

35% of the projected $135.3 billion smart home market is approximately
$47.355 billion.

This demonstrates multi-tool execution and multi-step reasoning.

---

## 10. When to Use Standard RAG

Standard RAG is appropriate when:

- Questions are primarily about enterprise documents.
- Retrieval is the main required operation.
- The system does not need external tools.
- A simple and predictable workflow is preferred.

Example:

"What are the key features of the SmartHome Hub?"

---

## 11. When to Use Agentic AI

Agentic AI is appropriate when:

- Different types of tools may be required.
- The question requires multiple operations.
- The system needs calculations.
- Web search may be required.
- Python execution may be required.
- Local files may need to be read.
- Multiple steps are required to answer a question.

Example:

"What is SmartTech Co.'s market share, and what would that percentage
represent in the projected market?"

---

## 12. Conclusion

Standard RAG provides an effective approach for answering questions from
enterprise documents.

Agentic AI extends this capability by allowing the system to dynamically
select and execute tools.

The implemented Enterprise Knowledge Assistant demonstrates that an agent
can:

- Retrieve enterprise information.
- Perform calculations.
- Search Wikipedia.
- Search the web.
- Execute Python.
- Read local files.
- Perform multi-step operations.
- Recover from tool errors.
- Maintain conversational context.
- Provide observable execution traces.

Therefore, the agentic architecture provides broader capabilities than
standard RAG while continuing to use the RAG pipeline as one of its tools.