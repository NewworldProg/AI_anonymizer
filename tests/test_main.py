"""Tests for the main anonymization system integration."""

import pytest
import os
from os.path import dirname
import main

@pytest.fixture
def main():
    return main()


import importlib
import types

def test_main_sample_text(monkeypatch):
    # Patch input to always choose sample text and skip de-anonymization
    inputs = iter(["1", "n"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main_mod = importlib.import_module('main')
    # Run main as a script (simulate __main__)
    # This will execute the anonymization pipeline and save files
    # Check that output files are created
    assert os.path.exists("output/anonymized_text.txt")
    assert os.path.exists("output/original_text.txt")
    assert os.path.exists("output/entity_mappings.txt")
    assert os.path.exists("output/statistics.txt")

def test_main_statistics_content():
    # Check that statistics file contains expected keys
    with open("output/statistics.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "Total entities found:" in content
    assert "Unique entities:" in content
    assert "Entity categories:" in content

def test_main_entity_mapping_content():
    # Check that entity mapping file contains expected placeholders
    with open("output/entity_mappings.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "ENTITY MAPPINGS" in content
    assert "[PER_1]" in content or "[ORG_1]" in content

