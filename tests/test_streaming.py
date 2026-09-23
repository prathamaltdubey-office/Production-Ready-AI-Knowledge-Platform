from chatbot.llm import stream_response


def test_stream_response_returns_chunks():
    chunks = list(stream_response("Explain customer churn in one short sentence."))

    assert len(chunks) > 0

    full_response = "".join(chunks)

    assert len(full_response) > 0
