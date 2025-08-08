"""Tests for TextDeanonymizer component."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from components.deanonymizer import TextDeanonymizer

@pytest.fixture
def processor():
    return TextDeanonymizer()

def test_deanonymize_text(processor):
    # Test basic deanonymization
    anonymized = "Hello [PER_1], how are you?"
    expected = "Hello John Smith, how are you?"
    entity_mapping = {
        '[PER_1]': 'John Smith'
    }
    result = processor.deanonymize_text(anonymized, entity_mapping=entity_mapping)
    assert result == expected

def test_deanonymize_multiple_placeholders(processor):
    # Test basic deanonymization with multiple placeholders
    anonymized = "Contact [PER_1] at [ORG_1] in [LOC_1]."
    expected = "Contact John Smith at Acme Corporation in New York."
    entity_mapping = {
        '[PER_1]': 'John Smith',
        '[ORG_1]': 'Acme Corporation',
        '[LOC_1]': 'New York'
    }
    result = processor.deanonymize_text(anonymized, entity_mapping=entity_mapping)
    assert result == expected

def test_deanonymize_no_placeholders(processor):
    # Test basic deanonymization with no placeholders
    anonymized = "No placeholders here."
    expected = "No placeholders here."
    entity_mapping = {
        '[PER_1]': 'John Smith'
    }
    result = processor.deanonymize_text(anonymized, entity_mapping=entity_mapping)
    assert result == expected

def test_deanonymize_empty_text(processor):
    anonymized = ""
    expected = ""
    entity_mapping = {
        '[PER_1]': 'John Smith'
    }
    result = processor.deanonymize_text(anonymized, entity_mapping=entity_mapping)
    assert result == expected

def test_deanonymize_missing_placeholder(processor):
    # Test deanonymization with text containing a missing placeholder
    anonymized = "Hello [PER_1] and [PER_999]."
    expected = "Hello John Smith and [PER_999]."
    entity_mapping = {
        '[PER_1]': 'John Smith'
    }
    result = processor.deanonymize_text(anonymized, entity_mapping=entity_mapping)
    assert result == expected

   