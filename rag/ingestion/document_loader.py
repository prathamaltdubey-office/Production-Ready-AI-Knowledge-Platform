from pathlib import Path

import pdfplumber
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}


def _format_table_as_markdown(table: list[list]) -> str:
    """
    Convert a pdfplumber-extracted table into a Markdown table
    string, which preserves row/column relationships far better
    than flattened plain text.
    """

    if not table or not table[0]:
        return ""

    # Replace None cells with empty strings.
    cleaned_rows = [[cell if cell is not None else "" for cell in row] for row in table]

    header = cleaned_rows[0]
    separator = ["---"] * len(header)
    body_rows = cleaned_rows[1:]

    lines = [
        "| " + " | ".join(str(cell).strip() for cell in header) + " |",
        "| " + " | ".join(separator) + " |",
    ]

    for row in body_rows:
        lines.append("| " + " | ".join(str(cell).strip() for cell in row) + " |")

    return "\n".join(lines)


def _load_pdf_with_tables(file_path: Path) -> list[Document]:
    """
    Load a PDF page by page, extracting both regular text and
    any tables. Tables are converted to Markdown format so their
    row/column structure survives, instead of being flattened
    into a scrambled sequence of words.
    """

    documents = []

    with pdfplumber.open(str(file_path)) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            # Extract tables first, and note their bounding boxes
            # so we can exclude that text from the plain-text extraction
            # to avoid duplicating the same content twice.
            tables = page.extract_tables()

            page_text = page.extract_text() or ""

            content_parts = []

            if page_text.strip():
                content_parts.append(page_text.strip())

            for table_index, table in enumerate(tables, start=1):
                markdown_table = _format_table_as_markdown(table)

                if markdown_table:
                    content_parts.append(
                        f"\n[Table {table_index} on page {page_number}]\n"
                        f"{markdown_table}"
                    )

            combined_content = "\n\n".join(content_parts)

            if combined_content.strip():
                documents.append(
                    Document(
                        page_content=combined_content,
                        metadata={
                            "source": str(file_path),
                            "page": page_number,
                        },
                    )
                )

    return documents


def load_document(file_path: str):
    """
    Load a single TXT, Markdown, or PDF document.

    PDFs are loaded with table-aware extraction: any tables on
    a page are converted to Markdown format to preserve their
    row/column structure, alongside the page's regular text.

    Args:
        file_path: Path to the document.

    Returns:
        List of LangChain Document objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    if extension == ".pdf":
        return _load_pdf_with_tables(path)

    # TXT / Markdown → normal text loading.
    loader = TextLoader(
        str(path),
        encoding="utf-8",
    )

    return loader.load()


def load_all_documents(
    directory: str = "documents",
):
    """
    Load all supported documents from a directory.

    Supported formats:
        TXT, Markdown, PDF.

    Args:
        directory: Directory containing documents.

    Returns:
        Combined list of LangChain Document objects.
    """

    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(f"Document directory not found: {directory_path}")

    all_documents = []

    for file_path in directory_path.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        documents = load_document(str(file_path))

        all_documents.extend(documents)

    return all_documents
