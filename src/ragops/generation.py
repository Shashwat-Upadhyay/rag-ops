"""Answer generation. Uses Gemini if GEMINI_API_KEY is set, otherwise a simple extractive answer."""
import os
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

NO_ANSWER = "I could not find this in the company documents."


def build_prompt(template: str, question: str, chunks: list[dict]) -> str:
    ctx = "\n\n".join(f"[{c['source']}] {c['text']}" for c in chunks)
    return template.format(context=ctx, question=question)


def generate_answer(question: str, chunks: list[dict], template: str, cfg: dict) -> tuple[str, str]:
    """Returns (answer, mode) where mode is 'gemini' or 'extractive'."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        try:
            from google import genai

            client = genai.Client(api_key=key)
            resp = client.models.generate_content(
                model=cfg["llm"]["model"], contents=build_prompt(template, question, chunks))
            return (resp.text or NO_ANSWER).strip(), "gemini"
        except Exception as e:  # network/quota errors: fall back, don't crash
            print(f"[generation] Gemini failed, using extractive answer: {e}")
    best = chunks[0]
    return f"According to {best['source']}: {best['text']}", "extractive"


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in ENGLISH_STOP_WORDS and len(t) > 2}


def groundedness(answer: str, chunks: list[dict]) -> float:
    """Share of the answer's content words that appear in the retrieved context (0..1).
    A cheap lexical proxy: low values suggest the answer may contain unsupported content."""
    a = _tokens(answer)
    if not a:
        return 0.0
    ctx = _tokens(" ".join(c["text"] for c in chunks))
    return round(len(a & ctx) / len(a), 3)
