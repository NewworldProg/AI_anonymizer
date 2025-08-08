"""Tests for StatisticsGenerator component."""

import pytest
from components.statistics_generator import StatisticsGenerator

@pytest.fixture
def statistics_generator():
    return StatisticsGenerator()

from collections import namedtuple

EntityMatch = namedtuple('EntityMatch', ['text', 'label', 'start', 'end', 'confidence'])

# input EntityMatch data
def test_statistics_generator_basic(statistics_generator):
    entities = [
        EntityMatch('John Smith', 'PER', 0, 10, 0.95),
        EntityMatch('Acme Corp', 'ORG', 11, 20, 0.90),
        EntityMatch('New York', 'LOC', 21, 30, 0.85),
        EntityMatch('John Smith', 'PER', 31, 41, 0.80)
    ]
    entity_mapping = {
        '[PER_1]': 'John Smith',
        '[ORG_1]': 'Acme Corp',
        '[LOC_1]': 'New York'
    }
    stats = statistics_generator.generate_statistics(entities, entity_mapping)
    assert stats['total_entities'] == 4
    assert stats['unique_entities'] == 3
    assert stats['by_category']['PER'] == 2
    assert stats['by_category']['ORG'] == 1
    assert stats['by_category']['LOC'] == 1
    assert 'PER' in stats['entity_types_found']
    assert 'ORG' in stats['entity_types_found']
    assert 'LOC' in stats['entity_types_found']
    assert stats['confidence_stats']['PER']['average confidence'] == (0.95 + 0.80) / 2
    assert stats['confidence_stats']['PER']['min confidence'] == 0.80
    assert stats['confidence_stats']['PER']['max confidence'] == 0.95
    # output results of basic statistics generation

    # input empty entities and mapping
def test_statistics_generator_empty_entities(statistics_generator):
    entities = []
    entity_mapping = {'[PER_1]': 'John Smith'}
    stats = statistics_generator.generate_statistics(entities, entity_mapping)
    assert stats['total_entities'] == 0
    assert stats['unique_entities'] == 1
    assert stats['by_category'] == {}
    assert stats['confidence_stats'] == {}
    assert stats['entity_types_found'] == []
    # output results of empty entities and mapping
