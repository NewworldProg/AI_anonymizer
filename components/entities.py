"""
Core entity data structures for the anonymization system.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EntityMatch:                                  # Represents a detected entity
    """Represents a detected entity match."""
    text: str
    label: str
    start: int
    end: int
    confidence: float
    
    def __hash__(self):
        """Create a hash for the entity so that it can check if its unique."""
        return hash((self.text.lower(), self.label))
    
    def __eq__(self, other):
        """Check equality between entities."""
        if not isinstance(other, EntityMatch): # checks if other can be compared to self
            return False
        return (self.text.lower() == other.text.lower() and # checks if text and label are the same
                self.label == other.label)


@dataclass
class AnonymizationResult:
    """Result of text anonymization."""
    anonymized_text: str
    statistics: Dict[str, Any]
    entity_mapping: Dict[str, str]
    original_entities: list = None
    
    def __post_init__(self):
        if self.original_entities is None:
            self.original_entities = []
