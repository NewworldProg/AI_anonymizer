"""Tests for EntityDetector component."""



import pytest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.entities import EntityMatch
from components.entity_detector import EntityDetector
from components import EntityMapper

# Remove the old anonymize_text helper, use only the one inside the test

@pytest.fixture
def detector():
    return EntityDetector()


# input text for testing regex detection
def test_regex_detection_email(detector):
    text = "Contact: john.doe@example.com"
    entities = detector._detect_entities_regex(text)
    emails = [e for e in entities if e.label == 'EMAIL']
    assert any('john.doe@example.com' in e.text for e in emails)
# output results of email detection

# input text for testing regex detection
def test_regex_detection_phone(detector):
    text = "Call us at 555-123-4567."
    entities = detector._detect_entities_regex(text)
    phones = [e for e in entities if e.label == 'PHONE']
    assert any('555-123-4567' in e.text for e in phones)
# output results of phone detection

# input text for testing regex detection
def test_regex_detection_url(detector):
    text = "Visit https://example.com for info."
    entities = detector._detect_entities_regex(text)
    urls = [e for e in entities if e.label == 'URL']
    assert any('https://example.com' in e.text for e in urls)
# output results of URL detection

# input mock text for testing NER detection
def test_ner_detection_mock(detector):
    entities = detector._detect_entities_ner('John Doe')
    assert len(entities) == 1
    assert entities[0].text == 'John Doe'
    assert entities[0].label == 'PER'
# output results of NER detection

# input mock text for testing NER deduplication
def test_deduplication_exact(detector):
    entities = [
        EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.99),
        EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.98),
    ]
    deduped = detector._deduplicate_entities(entities)
    assert len(deduped) == 1
# output results of deduplication of same entities

# input mock text for testing NER deduplication
def test_deduplication_overlap(detector):
    entities = [
        EntityMatch(text='John', label='PER', start=0, end=4, confidence=0.90),
        EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.99),
    ]
    deduped = detector._deduplicate_entities(entities)
    assert len(deduped) == 1
    assert deduped[0].text == 'John Doe'
# output results of of deduplication of overlapping entities




