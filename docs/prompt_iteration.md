# Prompt Iteration History

## Overview

The chatbot's system prompt (`chatbot/prompts.py`) evolved to its
current form to solve specific, observable failure modes. This
document reconstructs that iteration based on the defensive rules
present in the final prompt — each rule exists because an earlier,
simpler version of the prompt failed in that specific way.

---

## V1 — Baseline prompt

**Approach:** A simple instruction asking the LLM to answer questions
about the churn prediction project and "return your answer as JSON."

**Problem observed:** The LLM did not reliably return valid JSON.
Common failures included:
- Wrapping the JSON in Markdown code fences (` ```json ... ``` `)
- Adding a sentence of explanation before or after the JSON object
- Occasionally returning plain prose with no JSON structure at all

This made the response unparseable by the backend, which expects a
strict `{answer, topic, confidence}` structure.

---

## V2 — Explicit JSON formatting rules

**Change:** Added explicit, repeated constraints:
- "Do NOT put brackets, Markdown, or extra text around the JSON."
- "Return ONLY the JSON object."
- Provided a concrete example of valid output.

**Result:** Formatting became reliable for well-formed questions.

**New problem observed:** The `confidence` field, which should be a
float between 0 and 1, sometimes contained unexpected values —
including non-numeric content (e.g., a URL-like string) when the
model was uncertain or confused about what belongs in that field.

---

## V3 — Field-level type constraints + hallucination guard

**Change:** Added explicit per-field rules:
- `"confidence" must be a number between 0 and 1.`
- `"Do NOT put a URL inside the confidence field."`
- `"Do not invent prediction results."` — added after observing the
  chatbot would sometimes generate a plausible-looking churn
  prediction and probability even when no actual ML model had been
  run, blurring the line between the chatbot's conversational
  answers and the FastAPI `/predict` endpoint's real output.

**Result:** This is the current production prompt. It enforces:
1. Strict JSON-only output (no wrapping, no prose)
2. Explicit type constraints per field
3. A hard rule against fabricating prediction results, keeping the
   chatbot's role (explaining concepts) clearly separated from the
   ML pipeline's role (generating real predictions)

---

## How future iterations would be verified

For a production version, each prompt change would ideally be
validated against a fixed set of test questions before and after
the change, checking:
- JSON parses successfully on every response (100% target)
- `confidence` is always a valid float in range
- No prediction-shaped content appears unless a real model was
  actually invoked

This was not formally automated in the current version — test
questions were run manually during development rather than as a
repeatable regression suite. A natural next step would be adding
an automated prompt-regression test file (e.g.,
`tests/test_prompt_compliance.py`) that re-runs a fixed question
set on every prompt change and asserts the JSON contract holds.

---

## Known limitation

This document reconstructs the reasoning behind the current
prompt's rules rather than reflecting a formally logged v1→v2→v3
change history captured during development. Future prompt changes
to this project should be logged directly in this file as they
happen, with the specific failing example and the fix, rather than
reconstructed after the fact.