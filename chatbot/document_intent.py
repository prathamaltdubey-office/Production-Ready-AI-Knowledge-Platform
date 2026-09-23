import re

DOCUMENT_LIST_PATTERNS = [
    r"\bwhat (pdfs?|documents?|files?) do you have\b",
    r"\bhow many (pdfs?|documents?|files?)\b",
    r"\bwhich (pdfs?|documents?|files?)\b",
    r"\blist (the |all )?(pdfs?|documents?|files?)\b",
    r"\bwhat (pdfs?|documents?|files?) (are|is) (available|uploaded|indexed)\b",
    r"\bshow me (the |all )?(pdfs?|documents?|files?)\b",
    r"\b(give|tell) me (the )?names? of (the |all )?(pdfs?|documents?|files?)\b",
    r"\bname(s)? of (the |all )?(pdfs?|documents?|files?)\b",
    r"\b(pdfs?|documents?|files?) (available|uploaded|present|here)\b",
]


def is_document_list_request(message: str) -> bool:
    """
    Detect whether the user is asking a meta-question about
    which documents exist, rather than a content question
    that should go through RAG.
    """

    lowered = message.lower().strip()

    return any(re.search(pattern, lowered) for pattern in DOCUMENT_LIST_PATTERNS)
