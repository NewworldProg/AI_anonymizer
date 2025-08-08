"""
Core entity data structures for the anonymization system.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EntityMatch:                                  # object that holds information about a detected entity
    """Represents a detected entity match."""
    text: str
    label: str
    start: int
    end: int
    confidence: float
    
    def __hash__(self):
        # Create a hash for the entity so that it can check if its unique.
        return hash((self.text.lower(), self.label))
    
    def __eq__(self, other):
        # Check equality between entities.
        if not isinstance(other, EntityMatch): # checks if other can be compared to self
            return False
        return (self.text.lower() == other.text.lower() and # checks if text and label are the same
                self.label == other.label)

