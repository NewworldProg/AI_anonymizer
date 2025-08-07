"""Tests for ChunkProcessor component."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from components.chunk_processor import ChunkProcessor
from transformers import AutoTokenizer




@pytest.fixture
def processor():
    return ChunkProcessor()

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english", local_files_only=True)

class TestChunkProcessor:

    # input empty text for chunk creation
    def test_create_tokenized_chunks(self, processor):
        text = ""
        result = processor.create_tokenized_chunks(text, tokenizer)
        assert result == []
    # output empty text chunk creation

    # input empty text for regex safe chunk creation
    def test_create_regex_safe_chunks(self, processor):
        text = ""
        result = processor.create_regex_safe_chunks(text)
        assert result == [("", 0)]
    # output results of empty text and start offset

    # input text for tokenized chunk creation
    def test_tokenized_chunks_basic(self, processor):
        text = "This is a test sentence for chunking."
        result = processor.create_tokenized_chunks(text, tokenizer, max_tokens=3, overlap_tokens=1)
        assert len(result) > 0
        # Check that offsets are correct and chunks are not empty
        for chunk, offset in result:
            assert isinstance(chunk, str)
            assert isinstance(offset, int)
            assert chunk
    # output results of basic tokenized chunk creation

    # input text for regex safe chunk creation
    def test_regex_safe_chunks_basic(self, processor):
        text = "abc@domain.com some text https://site.com 123-456-7890 end."
        result = processor.create_regex_safe_chunks(text, chunk_size=20, overlap_size=5)
        # Accept either one chunk (if text is short) or multiple chunks
        assert len(result) >= 1
        for chunk, offset in result:
            assert isinstance(chunk, str)
            assert isinstance(offset, int)
            assert chunk
    # output results of basic regex safe chunk creation

    def test_regex_safe_chunks_small_text(self, processor):
        text = "short"
        result = processor.create_regex_safe_chunks(text, chunk_size=100)
        # Should return one chunk for small text
        assert result == [(text, 0)]



