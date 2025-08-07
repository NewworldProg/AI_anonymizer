"""Tests for Anonymizer component."""

import pytest
from components.anonymizer import Anonymizer
from components.entity_mapper import EntityMapper
from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])

def test_anonymize_basic():
    text = "John Smith works at Acme Corp."
    entities = [
        EntityMatch("John Smith", "PER", 0, 10, 0.99),
        EntityMatch("Acme Corp", "ORG", 20, 29, 0.95)
    ]
    mapper = EntityMapper()
    anonymizer = Anonymizer(text, entities, mapper)
    result = anonymizer.result_text
    filtered = anonymizer.filtered_entities
    assert "[PER_1]" in result
    assert "[ORG_1]" in result
    assert len(filtered) == 2

def test_anonymize_no_entities():
    text = "No entities here."
    entities = []
    mapper = EntityMapper()
    anonymizer = Anonymizer(text, entities, mapper)
    result = anonymizer.result_text
    filtered = anonymizer.filtered_entities
    assert result == text
    assert filtered == []