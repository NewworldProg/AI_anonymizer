"""Tests for EntityMapper component."""

import pytest
from components.entity_mapper import EntityMapper

@pytest.fixture
def entity_mapper():
    return EntityMapper()

from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])

def test_get_or_create_placeholder_basic(entity_mapper):
    # Test basic placeholder creation and mapping
    entity1 = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity2 = EntityMatch('Acme Corp', 'ORG', 11, 20, 0.95)
    placeholder1 = entity_mapper.get_or_create_placeholder(entity1)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity2)
    assert placeholder1 == '[PER_1]'
    assert placeholder2 == '[ORG_1]'
    mapping = entity_mapper.get_mapping()
    assert mapping[placeholder1] == 'John Smith'
    assert mapping[placeholder2] == 'Acme Corp'

def test_get_or_create_placeholder_consistency(entity_mapper):
    # Test that the same entity always gets the same placeholder
    entity = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    placeholder1 = entity_mapper.get_or_create_placeholder(entity)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity)
    assert placeholder1 == placeholder2

def test_get_or_create_placeholder_multiple_same_label(entity_mapper):
    # Test that multiple entities with the same label get unique placeholders
    entity1 = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity2 = EntityMatch('Mary Johnson', 'PER', 11, 21, 0.98)
    placeholder1 = entity_mapper.get_or_create_placeholder(entity1)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity2)
    assert placeholder1 == '[PER_1]'
    assert placeholder2 == '[PER_2]'

def test_get_mapping_thread_safety(entity_mapper):
    # check safety if get_mapping is called from multiple threads
    entity = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity_mapper.get_or_create_placeholder(entity)
    mapping1 = entity_mapper.get_mapping()
    mapping2 = entity_mapper.get_mapping()
    assert mapping1 == mapping2
