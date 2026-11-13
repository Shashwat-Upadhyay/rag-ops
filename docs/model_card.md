# Model Card: RAGOps Retriever + Answer Generator

**Purpose / intended use.** Answer employee questions about HR, IT, finance and onboarding using only documents
uploaded by HR. Every answer shows its source documents. When nothing relevant is found it says so.

**Not intended for.** Legal, medical or disciplinary decisions; questions about individual employees; anything not covered
by the uploaded documents. Employees should confirm important decisions (e.g. leave disputes) with HR.

**System.** Document chunks are retrieved with one of three retrievers (TF-IDF baseline, dense `BAAI/bge-small-en-v1.5`,
hybrid). The best one on the evaluation set is promoted through the MLflow Model Registry (alias `production`).
Answers are written by Gemini (optional) with a versioned prompt (`configs/prompts.yaml`), or extracted directly from the
top chunk when no API key is set.

**Evaluation.** `data/eval/eval_set.json` (12 questions: 9 in-scope, 3 out-of-scope). Metrics: hit-rate@k, MRR,
context-recall (expected keywords found in retrieved text), decision-accuracy (answers in-scope, refuses out-of-scope),
latency. A model is promoted only if it passes the quality gate in `configs/config.yaml`.
**Limitation:** the eval set is tiny and written by the developer, so scores are optimistic. Grow it from real questions.

**Explainability.** `/explain` uses LIME to show which words of the question drove the retrieval match.

**Groundedness.** Lexical proxy (share of answer words present in the retrieved text). It catches obvious
hallucinations but cannot detect paraphrased or subtly wrong statements.

**Fairness.** No demographic variables are used or predicted, so group-fairness metrics do not apply. Residual risk:
retrieval can favour documents written in the style/language of the question; documents are English only.

**Privacy.** Question text is NOT stored. Only per-query numbers (length, score, answered, latency) are logged for monitoring.
HR must not upload documents containing personal data of individual employees. Uploads are protected by a shared HR token
(demo-grade security: use real authentication before production).

**Known risks.** Outdated documents produce outdated answers (documents are versioned; re-upload to update). The LLM can
still make mistakes even with context. Thumbs-down feedback is tracked on the Grafana dashboard.
