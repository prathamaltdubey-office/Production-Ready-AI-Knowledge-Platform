# Retrieval and Generation Evaluation Report

## 1. Overview

The Enterprise Knowledge Assistant uses a Retrieval-Augmented Generation
(RAG) pipeline to retrieve relevant information from enterprise documents
before generating an answer.

The retrieval pipeline was evaluated using Recall@K at different retrieval
depths.

The generation pipeline was evaluated using a predefined question and
expected-keyword evaluation dataset.

---

## 2. Retrieval Evaluation

### Evaluation Metric

Recall@K was used to evaluate retrieval performance.

Recall@K measures whether the relevant document information was retrieved
within the top K retrieved results.

Higher Recall@K indicates that the retriever is more likely to retrieve the
information required to answer the user's question.

---

## 3. Retrieval Results

The retrieval system was evaluated at three retrieval depths.

| Retrieval Depth | Recall |
|---|---:|
| Recall@3 | 62.50% |
| Recall@5 | 75.00% |
| Recall@7 | 100.00% |

### Results

Recall increased as the number of retrieved documents increased:

- Recall@3: 62.50%
- Recall@5: 75.00%
- Recall@7: 100.00%

The best evaluated retrieval depth was:

**K = 7**

At K=7, the evaluation dataset achieved 100% recall.

---

## 4. Retrieval Optimization

The experiment demonstrates the effect of retrieval depth on recall.

Using only three retrieved results resulted in a Recall@3 of 62.50%.

Increasing the retrieval depth to five results improved recall to 75.00%.

Increasing the retrieval depth to seven results achieved 100.00% recall.

Therefore, K=7 was selected as the best retrieval depth among the tested
configurations.

---

## 5. Generation Evaluation

The generated answers were evaluated using a predefined evaluation dataset.

The evaluation dataset contained eight questions covering:

- Customer churn
- Customer churn risk
- Customer retention
- SmartHome Hub features
- Smart home market size
- SmartTech Co. market share
- Marketing strategy
- SmartHome Hub next steps

For each question, expected keywords were defined.

An answer was considered successful when at least 50% of the expected
keywords were present in the generated response.

---

## 6. Generation Results

All eight evaluation queries successfully met the evaluation threshold.

| Metric | Result |
|---|---:|
| Total queries | 8 |
| Successful queries | 8 |
| Failed queries | 0 |
| Generation Success Rate | 100.00% |

Every evaluated query achieved a content score of 1.00.

---

## 7. Example Evaluation

### Query

What are the key features of the SmartHome Hub?

### Expected information

- Universal compatibility
- AI-powered assistant
- Enhanced security

### Result

All expected keywords were found in the generated answer.

Content Score:

**1.00**

Result:

**PASS**

---

## 8. Grounded Response Evaluation

The RAG system was also tested with a question that was not covered by the
enterprise documents.

Example:

What is the population of Mars?

The system responded that the information was not available in the
provided documents rather than inventing an answer.

This demonstrates that the generation pipeline is grounded in the retrieved
document context and can reject unsupported questions.

---

## 9. Retrieval and Generation Summary

The evaluation produced the following results:

### Retrieval

Recall@3:

**62.50%**

Recall@5:

**75.00%**

Recall@7:

**100.00%**

Best retrieval depth:

**K=7**

### Generation

Successful queries:

**8 / 8**

Generation Success Rate:

**100.00%**

---

## 10. Conclusion

The retrieval evaluation shows that increasing retrieval depth improved
recall for the evaluated dataset.

Among the tested configurations, K=7 achieved the highest recall at 100%.

The generation evaluation achieved a 100% success rate across the eight
test questions.

The additional out-of-context test demonstrated that the system can avoid
fabricating information when the requested information is not present in
the enterprise document collection.

These results demonstrate effective retrieval optimization and grounded
response generation for the Enterprise Knowledge Assistant.