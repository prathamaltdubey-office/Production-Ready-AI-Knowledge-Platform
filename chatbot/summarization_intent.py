import re

SUMMARY_PATTERNS = [
    r"\bsummar(y|ize|ise)\b",
    r"\btable of contents\b",
    r"\btl;?dr\b",
    r"\bgive me (an? )?(overview|outline)\b",
    r"\bwhat is this (pdf|document|file) about\b",
    r"\bwhat does this (pdf|document|file) (say|cover|contain)\b",
]


def is_summary_request(message: str) -> bool:
    """
    Detect whether the user is asking for a whole-document
    summary or outline, which requires reading the full
    document rather than relying on chunk retrieval.
    """

    lowered = message.lower().strip()

    return any(re.search(pattern, lowered) for pattern in SUMMARY_PATTERNS)
