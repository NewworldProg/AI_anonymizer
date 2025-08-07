"""Tests for Anonymizer component."""

import pytest
from components.anonymizer import Anonymizer
from components.entity_mapper import EntityMapper
from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])
# input text, entities, and mapper for testing with mocked data
def test_anonymize_basic():
    text = "John Smith works at Acme Corp."
    entities = [
        EntityMatch("John Smith", "PER", 0, 10, 0.99),
        EntityMatch("Acme Corp", "ORG", 20, 29, 0.95)
    ]
    mapper = EntityMapper()

    # Initialize anonymizer with text, entities, and mapper
    anonymizer = Anonymizer(text, entities, mapper)
    anonymizer.anonymize()
    result = anonymizer.result_text
    filtered = anonymizer.filtered_entities
    assert "[PER_1]" in result
    assert "[ORG_1]" in result
    assert len(filtered) == 2
    # output anonymized text should contain placeholders

# input no entities in text
def test_anonymize_no_entities():
    text = "No entities here."
    entities = []
    mapper = EntityMapper()
    anonymizer = Anonymizer(text, entities, mapper)
    anonymizer.anonymize()
    result = anonymizer.result_text
    filtered = anonymizer.filtered_entities
    assert result == text
    assert filtered == []
# input are placeholders with special characters
def test_unicode_and_special_characters():
    """Test handling of unicode and special characters."""
    text = "José María works at Café François & Co. 北京大学"
    entities = [
        EntityMatch("José María", "PER", 0, 10, 0.95),
        EntityMatch("Café François & Co.", "ORG", 20, 39, 0.90),
        EntityMatch("北京大学", "ORG", 41, 45, 0.85),
    ]
    mapper = EntityMapper()
    anonymizer = Anonymizer(text, entities, mapper)
    anonymizer.anonymize()
    result = anonymizer.result_text
    
    assert "[PER_1]" in result
    assert "[ORG_1]" in result
    assert "[ORG_2]" in result
# output should be anonymized text with placeholders