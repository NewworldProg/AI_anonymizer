"""
Components package for text anonymization and entity detection.

This package provides modular components for:
- Entity detection using NER models
- Text chunking for large documents
- Entity mapping to placeholders
- Statistics generation
- Deanonymization capabilities
"""
from .input_text import InputTextHandler
from .entity_detector import EntityDetector
from .chunk_processor import ChunkProcessor
from .entity_mapper import EntityMapper
from .statistics_generator import StatisticsGenerator
from .deanonymizer import TextDeanonymizer
from .entities import EntityMatch
from .anonymizer import Anonymizer

__all__ = [
    'InputTextHandler',
    'EntityDetector',
    'ChunkProcessor', 
    'EntityMapper',
    'StatisticsGenerator',
    'TextDeanonymizer',
    'EntityMatch',
    'AnonymizationResult',
    'Anonymizer'
]

__version__ = "1.0.0"
