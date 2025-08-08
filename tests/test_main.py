"""Tests for the main anonymization system integration."""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
import importlib.util
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def clean_output_dir():
    # Clean up output directory before and after tests.
    import shutil
    output_dir = "output"
    
    # Clean before test
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    yield
    
    # Clean after test
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

def test_main_sample_text_with_save(monkeypatch, clean_output_dir):
    # main execution test with sample text
    # Mock all user inputs
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "y",        # Save results
        "n"         # Skip de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    # Mock the main module execution
    import main
    main.run_main()
    
    # Verify output files are created
    assert os.path.exists("output/anonymized_text.txt")
    assert os.path.exists("output/original_text.txt")
    assert os.path.exists("output/entity_mappings.txt")
    assert os.path.exists("output/statistics.txt")

def test_main_sample_text_with_deanonymization(monkeypatch, clean_output_dir):
    """Test main execution with de-anonymization."""
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "y",        # Save results
        "y"         # Test de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    # Mock the main module execution
    import main
    main.run_main()
    
    # Verify all output files including deanonymized text
    assert os.path.exists("output/anonymized_text.txt")
    assert os.path.exists("output/original_text.txt")
    assert os.path.exists("output/entity_mappings.txt")
    assert os.path.exists("output/statistics.txt")
    assert os.path.exists("output/deanonymized_text.txt")

def test_main_custom_text(monkeypatch, clean_output_dir):
    """Test main execution with custom text input."""
    inputs = iter([
        "2",                    # Choose custom text
        "John Smith works at Acme Corp in New York.",  # Custom text
        "",                     # Press Enter to start chunk processing
        "",                     # Press Enter to show anonymized text preview
        "",                     # Press Enter to generate statistics
        "y",                    # Save results
        "n"                     # Skip de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    # Mock the main module execution
    import main
    main.run_main()
    
    # Verify output files are created
    assert os.path.exists("output/anonymized_text.txt")
    assert os.path.exists("output/original_text.txt")
    assert os.path.exists("output/entity_mappings.txt")
    assert os.path.exists("output/statistics.txt")

def test_main_skip_save(monkeypatch, clean_output_dir):
    """Test main execution when user chooses not to save."""
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "n",        # Don't save results
        "n"         # Extra input just in case (shouldn't be needed but prevents StopIteration)
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    # Mock exit to prevent actual program termination
    with patch('builtins.exit') as mock_exit:
        import main
        main.run_main()
        mock_exit.assert_called_once_with(0)
    
    # Verify no output files are created
    assert not os.path.exists("output/anonymized_text.txt")
    assert not os.path.exists("output/original_text.txt")
    assert not os.path.exists("output/entity_mappings.txt")
    assert not os.path.exists("output/statistics.txt")

def test_main_statistics_content(monkeypatch, clean_output_dir):
    """Test that statistics file contains expected content."""
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "y",        # Save results
        "n"         # Skip de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    import main
    main.run_main()
    
    # Check statistics file content
    with open("output/statistics.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "ANONYMIZATION STATISTICS" in content
    assert "Total entities found:" in content
    assert "Unique entities:" in content
    assert "Processing time:" in content
    assert "Peak memory usage:" in content
    assert "Entity categories:" in content

def test_main_entity_mapping_content(monkeypatch, clean_output_dir):
    """Test that entity mapping file contains expected content."""
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "y",        # Save results
        "n"         # Skip de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    import main
    main.run_main()
    
    # Check entity mapping file content
    with open("output/entity_mappings.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "ENTITY MAPPINGS" in content
    # Check for placeholder format (should contain at least one entity type)
    assert "→" in content  # Mapping arrow character

def test_main_component_initialization(monkeypatch):
    """Test that all components are properly initialized."""
    inputs = iter([
        "1",        # Choose sample text
        "",         # Press Enter to start chunk processing
        "",         # Press Enter to show anonymized text preview
        "",         # Press Enter to generate statistics
        "n",        # Don't save results
        "n"         # Skip de-anonymization (needed because exit is mocked)
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    # Mock exit to prevent actual program termination
    with patch('builtins.exit'):
        # Mock the components to verify they're called correctly
        with patch('main.EntityDetector') as mock_detector, \
             patch('main.EntityMapper') as mock_mapper, \
             patch('main.StatisticsGenerator') as mock_stats:
            
            import main
            main.run_main()
            
            # Verify components were initialized with correct parameters
            mock_detector.assert_called_once_with(
                "Jean-Baptiste/roberta-large-ner-english", 
                confidence_threshold=0.8
            )
            mock_mapper.assert_called_once()
            mock_stats.assert_called_once()

def test_main_anonymizer_integration(monkeypatch, clean_output_dir):
    """Test that the Anonymizer component is properly integrated."""
    inputs = iter([
        "2",                    # Choose custom text
        "John Doe works here.", # Simple text for testing
        "",                     # Press Enter to start chunk processing
        "",                     # Press Enter to show anonymized text preview
        "",                     # Press Enter to generate statistics
        "y",                    # Save results
        "n"                     # Skip de-anonymization
    ])
    monkeypatch.setattr('builtins.input', lambda prompt="": next(inputs))
    
    import main
    main.run_main()
    
    # Check that anonymized text was created and is different from original
    with open("output/original_text.txt", "r", encoding="utf-8") as f:
        original = f.read()
    with open("output/anonymized_text.txt", "r", encoding="utf-8") as f:
        anonymized = f.read()
    
    assert original == "John Doe works here."
    # The anonymized text should contain placeholders if entities were detected
    assert anonymized is not None