"""Tests for InputTextHandler component."""

import pytest
from components.input_text import InputTextHandler

@pytest.fixture
def handler():
    return InputTextHandler()

def test_sample_text(monkeypatch, handler):
    # Patch input to choose sample text
    monkeypatch.setattr('builtins.input', lambda _: "1")
    text = handler.text_handler()
    assert isinstance(text, str)
    assert "Dear" in text or len(text) > 0

def test_custom_text(monkeypatch, handler):
    # Patch input to choose custom text and provide text
    inputs = iter(["2", "Hello world!"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    text = handler.text_handler()
    assert text == "Hello world!"

def test_file_text(tmp_path, monkeypatch, handler):
    # Create a temp file with some text
    file = tmp_path / "test.txt"
    file.write_text("File input test.", encoding="utf-8")
    inputs = iter(["3", str(file)])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    handler.default_file_path = None  # Ensure prompt for file path
    text = handler.text_handler()
    assert text == "File input test."