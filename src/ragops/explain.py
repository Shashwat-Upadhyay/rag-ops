"""LIME explanation: which words of the question made the retriever find a strong match?"""
import numpy as np


def explain_query(index, question: str, num_features: int = 6, num_samples: int = 150, seed: int = 42):
    from lime.lime_text import LimeTextExplainer

    def predict(texts):
        out = []
        for t in texts:
            s = float(np.clip(index.top_score(t), 0, 1)) if t.strip() else 0.0
            out.append([1 - s, s])
        return np.array(out)

    explainer = LimeTextExplainer(class_names=["weak_match", "strong_match"], random_state=seed)
    exp = explainer.explain_instance(question, predict, num_features=num_features,
                                     num_samples=num_samples, labels=(1,))
    return [{"term": w, "weight": round(float(v), 4)} for w, v in exp.as_list(label=1)]
