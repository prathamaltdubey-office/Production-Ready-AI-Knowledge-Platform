from pathlib import Path

from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


@tool
def file_reader(filename: str) -> str:
    """
    Read a text, Markdown, or PDF file from the documents directory.

    Args:
        filename: Name of the file inside the documents directory.

    Returns:
        File contents or an error message.
    """

    try:
        if not filename.strip():
            return "Error: filename cannot be empty."

        file_path = (DOCUMENTS_DIR / filename).resolve()

        # Prevent access outside the documents directory.
        if DOCUMENTS_DIR.resolve() not in file_path.parents:
            return "Error: access outside the documents directory is not allowed."

        if not file_path.exists():
            return f"Error: file not found: {filename}"

        if not file_path.is_file():
            return f"Error: path is not a file: {filename}"

        extension = file_path.suffix.lower()

        if extension in {".txt", ".md"}:
            return file_path.read_text(encoding="utf-8")

        if extension == ".pdf":
            return _read_pdf(file_path)

        return (
            f"Error: unsupported file type: {extension}. "
            "Supported types are .txt, .md, and .pdf."
        )

    except Exception as exc:
        return f"Error reading file: {exc}"


def _read_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""

    from pypdf import PdfReader

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""

        pages.append(f"--- Page {page_number} ---\n{text}")

    return "\n\n".join(pages)
