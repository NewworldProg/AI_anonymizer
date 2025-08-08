"""Tests for placeholder collision handling."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from components.entity_mapper import EntityMapper
from components.anonymizer import Anonymizer
from components.deanonymizer import TextDeanonymizer
from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])

@pytest.fixture
def entity_mapper():
    return EntityMapper()

def test_collision_safe_placeholder_generation(entity_mapper):
    """Test that placeholders avoid collisions with text content."""
    # Set text that contains natural placeholder-like patterns
    original_text = "The report mentions [PER_1] and references section [ORG_1] in the document."
    entity_mapper.set_original_text(original_text)
    
    # Create entities
    entity1 = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity2 = EntityMatch('Acme Corp', 'ORG', 11, 20, 0.95)
    
    # Get placeholders
    placeholder1 = entity_mapper.get_or_create_placeholder(entity1)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity2)
    
    # Verify placeholders don't match existing text patterns
    assert placeholder1 != '[PER_1]'  # Should skip this due to collision
    assert placeholder2 != '[ORG_1]'  # Should skip this due to collision
    
    # Verify they are still valid placeholders
    assert placeholder1.startswith('[PER_')
    assert placeholder1.endswith(']')
    assert placeholder2.startswith('[ORG_')
    assert placeholder2.endswith(']')

def test_end_to_end_collision_handling():
    # Text that contains natural placeholder-like patterns
    original_text = "John Smith works at [ORG_1] company and knows [PER_1] personally."
    
    # Mock entities (normally these would come from NER)
    entities = [
        EntityMatch('John Smith', 'PER', 0, 10, 0.99),
        EntityMatch('[ORG_1]', 'ORG', 20, 28, 0.85)  # This entity text looks like a placeholder
    ]
    
    # Anonymize using the proper pattern
    entity_mapper = EntityMapper()
    anonymizer = Anonymizer(original_text, entities, entity_mapper)
    anonymizer.anonymize()
    
    anonymized_text = anonymizer.result_text
    entity_mapping = entity_mapper.get_mapping()
    
    # Verify no confusion in the anonymization
    assert 'John Smith' not in anonymized_text
    # The original [ORG_1] should be replaced by a different placeholder due to collision detection
    # But the pattern [ORG_1] should still appear in some form (as part of text or as entity replacement)
    
    # Count placeholder occurrences to verify proper handling
    placeholder_count = anonymized_text.count('[')
    # Should have placeholders for entities, and collision-safe generation should work
    assert placeholder_count >= 2  # At least 2 placeholders (one for each entity)
    
    # Verify collision-safe placeholders were generated
    # John Smith should get a placeholder that doesn't conflict with existing text
    john_smith_placeholder = None
    org_entity_placeholder = None
    for placeholder, entity_text in entity_mapping.items():
        if entity_text == 'John Smith':
            john_smith_placeholder = placeholder
        elif entity_text == '[ORG_1]':  # The entity that looks like a placeholder
            org_entity_placeholder = placeholder
    
    # Verify placeholders were created and are collision-safe
    assert john_smith_placeholder is not None
    assert org_entity_placeholder is not None
    # John Smith should NOT get [PER_1] because that pattern exists in original text
    assert john_smith_placeholder != '[PER_1]'
    # The [ORG_1] entity should NOT get [ORG_1] because that would be the same as the entity text
    assert org_entity_placeholder != '[ORG_1]'
    
    # Deanonymize
    deanonymizer = TextDeanonymizer()
    restored_text = deanonymizer.deanonymize_text(anonymized_text, entity_mapping)
    
    # Verify restoration
    assert 'John Smith' in restored_text
    assert '[ORG_1]' in restored_text  # Original entity content preserved
    
def test_multiple_collision_scenarios(entity_mapper):
    """Test handling of multiple potential collisions."""
    # Text with many placeholder-like patterns
    original_text = """
    Document contains [PER_1], [PER_2], [ORG_1], and [LOC_1].
    Also has [PER_1], [ORG_1], and other patterns like [PER_3].
    """
    entity_mapper.set_original_text(original_text)
    
    # Create multiple entities
    entities = [
        EntityMatch('Alice', 'PER', 0, 5, 0.99),
        EntityMatch('Bob', 'PER', 6, 9, 0.98),
        EntityMatch('Carol', 'PER', 10, 15, 0.97),
        EntityMatch('Dave', 'PER', 16, 20, 0.96),
        EntityMatch('TechCorp', 'ORG', 21, 29, 0.95),
        EntityMatch('New York', 'LOC', 30, 38, 0.94)
    ]
    
    placeholders = []
    for entity in entities:
        placeholder = entity_mapper.get_or_create_placeholder(entity)
        placeholders.append(placeholder)
        
        # Verify no placeholder matches existing text
        assert placeholder not in original_text
    
    # Verify all placeholders are unique
    assert len(placeholders) == len(set(placeholders))
    
    # Verify proper formatting
    for placeholder in placeholders:
        assert placeholder.startswith('[')
        assert placeholder.endswith(']')
        assert '_' in placeholder
