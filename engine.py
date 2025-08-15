import re
import spacy
import tiktoken
from lemminflect import getAllLemmas


class AdvancedPromptOptimizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def optimize(self, prompt: str, aggressiveness: float = 0.7) -> tuple:
        """Optimize prompt with token counting"""
        optimized = self._apply_rules(prompt, aggressiveness)
        optimized = self._linguistic_optimize(optimized, aggressiveness)
        optimized = re.sub(r"\s+", " ", optimized).strip()

        try:
            orig_tokens = len(self.tokenizer.encode(prompt))
            new_tokens = len(self.tokenizer.encode(optimized))

        except:
            orig_tokens = len(prompt.split())
            new_tokens = len(optimized.split())

        return optimized, orig_tokens, new_tokens

    def _apply_rules(self, text: str, aggressiveness: float) -> str:
        rules = [
            (r"\b(please\s+)?(carefully|very|extremely)\b", "", 0.8),
            (r"\b(advantages and disadvantages)\b", "pros/cons", 0.9),
            (r"\boutput in JSON format\b", "JSON:", 1.0),
            (r"\b(for example|e\.g\.)\b", "ex:", 0.9),
            (r"\s{2,}", " ", 0.0),  # Always apply
        ]
        for pattern, repl, priority in rules:
            if priority >= aggressiveness:
                text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        return text

    def _linguistic_optimize(self, text: str, aggressiveness: float) -> str:
        if not text.strip():
            return text
        doc = self.nlp(text)
        optimized = []
        for token in doc:
            if token.pos_ == "VERB" and aggressiveness >= 0.8:
                noun_forms = getAllLemmas(token.text).get("NOUN")
                if noun_forms:
                    optimized.append(next(iter(noun_forms)))
            elif token.pos_ in ("NOUN", "PROPN", "NUM"):
                optimized.append(token.text)
            elif aggressiveness < 0.7:  # Keep more words at lower levels
                optimized.append(token.text)
        return " ".join(optimized)
