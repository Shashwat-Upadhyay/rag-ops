# Data Card

| Item | Description |
|---|---|
| Content | Company policy documents (sample: leave policy, VPN guide, expense policy, onboarding guide) written for this demo. Not real company data. |
| Source | Uploaded by HR through the HR Portal or placed in `data/raw/` |
| Formats | `.md`, `.txt`, `.pdf` (text-based PDFs; scanned PDFs need OCR and are rejected by validation if no text is extracted) |
| Versioning | `data/registry.json` stores a content hash and an integer version per document; DVC records dataset hashes in `dvc.lock`; each index stores a `docs_fingerprint` |
| Validation | Not empty, at least 20 words, no duplicate files (see `pipeline.validate`) |
| Eval data | `data/eval/eval_set.json`, hand-written Q&A with expected source document and keywords |
| Personal data | None in the sample. Real uploads must not contain employee personal data |
| Retention | Query log keeps numbers only (no question text) in `data/logs/queries.jsonl` |
