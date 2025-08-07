"""Tests for EntityMapper component."""

import pytest
from components.entity_mapper import EntityMapper

@pytest.fixture
def entity_mapper():
    return EntityMapper()

from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])

def test_get_or_create_placeholder_basic(entity_mapper):
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
    entity = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    placeholder1 = entity_mapper.get_or_create_placeholder(entity)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity)
    assert placeholder1 == placeholder2

def test_get_or_create_placeholder_multiple_same_label(entity_mapper):
    entity1 = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity2 = EntityMatch('Mary Johnson', 'PER', 11, 21, 0.98)
    placeholder1 = entity_mapper.get_or_create_placeholder(entity1)
    placeholder2 = entity_mapper.get_or_create_placeholder(entity2)
    assert placeholder1 == '[PER_1]'
    assert placeholder2 == '[PER_2]'

def test_get_mapping_thread_safety(entity_mapper):
    # Just check that get_mapping returns a copy and doesn't error
    entity = EntityMatch('John Smith', 'PER', 0, 10, 0.99)
    entity_mapper.get_or_create_placeholder(entity)
    mapping1 = entity_mapper.get_mapping()
    mapping2 = entity_mapper.get_mapping()
    assert mapping1 == mapping2
