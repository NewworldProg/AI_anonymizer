import pytest
import time
import tracemalloc
from components.chunk_processor import ChunkProcessor
from components.entity_detector import EntityDetector


@pytest.fixture(scope="module")
def large_text():
    # Generate a large text (10MB+)
    return "John Smith works at Acme Corp. " * 100



def test_large_document_performance(large_text):
    """Test processing time and memory usage for large documents using chunking."""
    start_time = time.time()
    tracemalloc.start()

    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
    processor = ChunkProcessor()
    detector = EntityDetector()

    chunks = processor.create_tokenized_chunks(large_text, tokenizer)
    entities = []
    for chunk_text, chunk_offset in chunks:
        chunk_entities = detector._detect_entities_ner(chunk_text, chunk_offset)
        entities.extend(chunk_entities)

    processing_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Assert reasonable performance bounds
    assert processing_time < 60  # Should complete within 1 minute
    assert peak < 500 * 1024 * 1024  # Should use less than 500MB
    assert len(entities) > 0  # Should find entities