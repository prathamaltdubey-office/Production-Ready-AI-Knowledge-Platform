from agent.tools.file_reader import file_reader


def main() -> None:
    """Test the file reader tool."""

    result = file_reader.invoke("sample.txt")

    print("=" * 60)
    print("FILE READER TOOL TEST")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
