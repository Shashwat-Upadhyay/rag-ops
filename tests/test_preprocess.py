from ragops.documents import chunk_text, clean_text, make_chunks


def test_clean_text_collapses_whitespace():
    assert clean_text("a   b\n\n\n\nc \x00 d") == "a b\n\nc d"


def test_chunk_overlap_and_size():
    text = " ".join(str(i) for i in range(100))
    chunks = chunk_text(text, chunk_size=30, overlap=10)
    assert all(len(c.split()) <= 30 for c in chunks)
    assert chunks[0].split()[-10:] == chunks[1].split()[:10]   # overlap kept
    assert " ".join(chunks).count("99") >= 1                  # nothing lost at the end


def test_make_chunks_keeps_source_and_version():
    chunks = make_chunks([{"source": "a.md", "text": "word " * 50, "version": 3}], 20, 5)
    assert chunks[0]["source"] == "a.md" and chunks[0]["doc_version"] == 3
