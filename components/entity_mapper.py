from typing import Dict
from collections import defaultdict
import threading
import re
from .entities import EntityMatch  # Import from dedicated entities module


class EntityMapper: # class for mapping entities to placeholders
    """Maintains consistent entity mappings across document chunks with thread-safety and collision detection."""
    
    def __init__(self): # constructor for entity mapper that will connect entities to placeholders
        self.entity_to_placeholder: Dict[EntityMatch, str] = {} # makes dictionary for holding entity as key and placeholder as value
        self.placeholder_to_entity: Dict[str, str] = {} # makes dictionary for holding placeholder as key and entity text as value
        self.counters: Dict[str, int] = defaultdict(int)    # makes counter for each entity label
        self._lock = threading.Lock()  # Thread-safe lock for concurrent access
        self.original_text = None  # Store original text to check for collisions

    def set_original_text(self, text: str):
        """Set the original text to check for placeholder collisions."""
        with self._lock:
            self.original_text = text

    def _generate_safe_placeholder(self, label: str, text: str) -> str:
        """Generate a placeholder that doesn't exist in the original text."""
        base_counter = self.counters[label] + 1
        
        while True:
            # Use bracket format for compatibility with expected output
            placeholder = f"[{label}_{base_counter}]"
            
            # Check if this placeholder already exists in mappings
            if placeholder in self.placeholder_to_entity:
                base_counter += 1
                continue
            
            # Check if this placeholder appears naturally in the original text
            if self.original_text and placeholder in self.original_text:
                base_counter += 1
                continue
            
            # Safe placeholder found
            self.counters[label] = base_counter
            return placeholder

    def get_or_create_placeholder(self, entity: EntityMatch) -> str: # function that will return existing placeholder or create new one for new entity
        """Get existing placeholder or create new one for entity (thread-safe)."""
        
        with self._lock:  # Ensure thread-safe access to shared state
            if entity in self.entity_to_placeholder:       # if the entity already has a placeholder (uses EntityMatch.__hash__)
                return self.entity_to_placeholder[entity]  # give it the same placeholder
            
            # Generate collision-safe placeholder
            placeholder = self._generate_safe_placeholder(entity.label, entity.text)

            self.entity_to_placeholder[entity] = placeholder # create a mapping entity to placeholder
            self.placeholder_to_entity[placeholder] = entity.text # create a mapping placeholder to entity text
            
            return placeholder # return the newly created placeholder
    
    def get_mapping(self) -> Dict[str, str]: # function for deanonymization
        """Get the complete placeholder to entity mapping (thread-safe)."""
        with self._lock:  # Ensure consistent snapshot of mappings
            return self.placeholder_to_entity.copy()    

