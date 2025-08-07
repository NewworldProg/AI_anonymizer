"""Tests for Entities module (EntityMatch class)."""

import pytest
from components.entities import EntityMatch

def test_entitymatch_basic_instantiation():
    # input all parameters for EntityMatch
    e = EntityMatch(text='Alice', label='PER', start=5, end=10, confidence=0.88)
    assert e.text == 'Alice'
    assert e.label == 'PER'
    assert e.start == 5
    assert e.end == 10
    assert e.confidence == 0.88
    # output results of instantiation check

def test_entitymatch_equality():
    # input Entries with the same text and label
    e1 = EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.99)
    e2 = EntityMatch(text='john doe', label='PER', start=10, end=18, confidence=0.95)
    assert e1 == e2
    # output results of __eq__ check


def test_entitymatch_inequality():
    # input Entities with different label should not be equal
    e1 = EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.99)
    e2 = EntityMatch(text='Jane Doe', label='PER', start=0, end=8, confidence=0.99)
    e3 = EntityMatch(text='John Doe', label='ORG', start=0, end=8, confidence=0.99)
    assert e1 != e2
    assert e1 != e3
    # output results of __eq__ check

def test_entitymatch_hash():
    # input Entities with the same text and label
    e1 = EntityMatch(text='John Doe', label='PER', start=0, end=8, confidence=0.99)
    e2 = EntityMatch(text='john doe', label='PER', start=10, end=18, confidence=0.95)
    assert hash(e1) == hash(e2)
    # output results of hash check


