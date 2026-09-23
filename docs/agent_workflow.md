# Agent Workflow Documentation

## 1. Overview

The Enterprise Knowledge Assistant uses an agentic AI architecture built with
LangChain and LangGraph.

The agent can select and use multiple tools depending on the user's question.

The implemented tools are:

1. Calculator
2. Wikipedia
3. DuckDuckGo Search
4. Python REPL
5. File Reader
6. Document Retriever

The agent uses a local open-source LLM through Ollama.

---

## 2. Architecture

The overall agent workflow is:

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
Tool Result
    |
    v
Agent
    |
    v
Final Answer

The agent decides which tool is appropriate based on the user's request.

---

## 3. Technology Stack

The agent uses the following technologies:

- Python
- LangChain
- LangGraph
- Ollama
- Qwen 2.5 7B
- FAISS / vector retrieval infrastructure
- Sentence Transformers
- Wikipedia
- DuckDuckGo Search

The LLM is executed locally using Ollama.

---

## 4. Available Tools

### 4.1 Calculator

The Calculator tool performs mathematical calculations.

Example:

User:

What is 125 multiplied by 48?

Agent:

Calculator

Result:

6000

The calculator also handles errors such as division by zero.

---

### 4.2 Wikipedia

The Wikipedia tool retrieves general factual information.

Example:

User:

What is artificial intelligence?

Agent:

Wikipedia

The retrieved information is then used to construct the final answer.

The tool also validates empty queries and returns an error instead of
executing an invalid request.

---

### 4.3 DuckDuckGo Search

The DuckDuckGo Search tool retrieves information from the web.

It is useful when the user requires web search or current information.

The tool validates empty search queries.

---

### 4.4 Python REPL

The Python REPL allows the agent to execute Python code.

It can be used for:

- calculations
- data processing
- programming tasks

The tool handles execution errors and rejects empty Python code.

---

### 4.5 File Reader

The File Reader reads supported local documents.

It supports the project documents such as:

- Markdown
- Text
- PDF

Example:

User:

Read sample.pdf.

Agent:

File Reader

The contents of the PDF are returned to the agent.

The tool also handles missing files and empty filenames.

---

### 4.6 Document Retriever

The Document Retriever connects the agent to the project's RAG pipeline.

It performs semantic retrieval against the enterprise document collection.

It is preferred for questions that can be answered using the enterprise
documents.

Example:

User:

What are the key features of the SmartHome Hub?

Agent:

Document Retriever

The retrieved document context is then used to generate the final answer.

---

## 5. Tool Selection

The agent selects tools according to the type of question.

| User Request | Tool |
|---|---|
| Mathematical calculation | Calculator |
| General factual information | Wikipedia |
| Current/web information | DuckDuckGo Search |
| Python/data processing | Python REPL |
| Read a local file | File Reader |
| Enterprise document question | Document Retriever |

The agent can also select multiple tools when a question requires multiple
operations.

---

## 6. Multi-Step Reasoning

The agent supports multi-step execution.

Example:

User:

What is SmartTech Co.'s market share according to the SmartHome Hub
document, and calculate what 35% of the projected $135.3 billion smart
home market would be?

The agent performs two operations:

Step 1:

Document Retriever

Retrieves:

SmartTech Co. market share = 35%

Step 2:

Calculator

Calculates:

0.35 × 135,300,000,000

Result:

47,355,000,000

Final answer:

SmartTech Co.'s market share is 35%, and 35% of the projected
$135.3 billion market is approximately $47.355 billion.

This demonstrates multi-tool and multi-step agent execution.

---

## 7. Memory

The agent supports conversational memory.

Example:

User:

What is the market share of SmartTech Co.?

Agent:

SmartTech Co. has a market share of 35%.

User:

What is the projected market size mentioned in the same document?

Agent:

The projected smart home market size is $135.3 billion.

The second question can be understood in the context of the previous
conversation.

---

## 8. Execution Tracing

Agent execution can be traced to inspect the sequence of operations.

Example:

STEP 1
User question

STEP 2
Agent selects Document Retriever and Calculator

STEP 3
Document Retriever returns the SmartTech Co. market share

STEP 4
Calculator calculates 35% of $135.3 billion

STEP 5
Agent generates the final answer

The trace records:

- messages
- selected tools
- tool arguments
- tool results
- final response

This makes the agent workflow observable and easier to debug.

---

## 9. Error Recovery

The agent handles tool errors without crashing.

### Division by zero

Input:

Calculate 100 divided by 0.

Calculator result:

Error calculating expression: division by zero

The agent provides a user-friendly response.

### Missing file

Input:

Read the file does_not_exist.txt.

File Reader result:

Error: file not found

The agent informs the user that the requested file does not exist.

### Empty search query

Input:

Search Wikipedia for an empty query.

Wikipedia result:

Error: search query cannot be empty.

The agent responds with a request for a valid search term.

This demonstrates error recovery and graceful handling of tool failures.

---

## 10. Standard RAG vs Agentic AI

The project compares a standard RAG pipeline with the agentic approach.

### Standard RAG

Standard RAG follows:

User Query
    |
    v
Retriever
    |
    v
Relevant Documents
    |
    v
LLM
    |
    v
Answer

It is mainly designed for answering questions using retrieved enterprise
documents.

### Agentic AI

Agentic AI follows:

User Query
    |
    v
Agent
    |
    +--> Calculator
    +--> Wikipedia
    +--> Web Search
    +--> Python REPL
    +--> File Reader
    +--> Document Retriever
    |
    v
Final Answer

The agent can decide which tool is required and can use multiple tools
during one request.

---

## 11. Comparison Results

The implementation was tested using three questions.

| Question | Standard RAG | Agentic AI |
|---|---|---|
| SmartHome Hub features | Answered | Answered |
| SmartTech Co. market share | Answered | Answered |
| 125 × 48 | Not available in documents | Calculated successfully |

The comparison demonstrates that standard RAG is focused on document
retrieval, while the agent can perform actions outside the document
collection.

---

## 12. Agent Workflow Summary

The implemented workflow supports:

- Tool selection
- Multi-step reasoning
- Multiple tool execution
- Conversational memory
- Execution tracing
- Error recovery
- Enterprise document retrieval

The resulting system acts as an Enterprise Knowledge Assistant capable of
combining RAG with multiple external and computational tools.