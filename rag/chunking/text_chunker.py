from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50


SECTION_HEADERS = [
    "Introduction",
    "Objectives",
    "Key Features",
    "Market Analysis",
    "Competitor Analysis",
    "Marketing Strategy",
    "Conclusion",
    "Next Steps",
]


def _split_pdf_sections(document: Document) -> list[Document]:
    """
    Split a PDF page into logical sections using known section headers.

    This preserves semantically related content together, improving
    retrieval quality for section-specific questions.
    """

    text = document.page_content

    sections = []

    current_lines = []

    for line in text.splitlines():

        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        # Remove page-number-only lines.
        if cleaned_line.isdigit():
            continue

        if cleaned_line in SECTION_HEADERS:

            if current_lines:
                content = "\n".join(current_lines).strip()

                if content:
                    sections.append(
                        Document(
                            page_content=content,
                            metadata=dict(document.metadata),
                        )
                    )

            current_lines = [cleaned_line]

        else:
            current_lines.append(cleaned_line)

    # Add final section.
    if current_lines:
        content = "\n".join(current_lines).strip()

        if content:
            sections.append(
                Document(
                    page_content=content,
                    metadata=dict(document.metadata),
                )
            )

    return sections


def chunk_documents(
    documents,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
):
    """
    Split documents into retrieval-friendly chunks.

    PDF documents are first divided into logical sections.
    Other documents use RecursiveCharacterTextSplitter.

    Args:
        documents: List of LangChain Document objects.
        chunk_size: Maximum chunk size.
        chunk_overlap: Overlap between chunks.

    Returns:
        List of chunked LangChain Document objects.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    final_chunks = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "",
        )

        # PDF → section-aware splitting.
        if source.lower().endswith(".pdf"):

            sections = _split_pdf_sections(document)

            for section in sections:

                # Keep small logical sections intact.
                if len(section.page_content) <= chunk_size:

                    final_chunks.append(section)

                else:

                    split_sections = text_splitter.split_documents([section])

                    final_chunks.extend(split_sections)

        # TXT / Markdown → normal recursive splitting.
        else:

            chunks = text_splitter.split_documents([document])

            final_chunks.extend(chunks)

    return final_chunks
