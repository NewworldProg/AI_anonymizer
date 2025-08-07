from typing import Dict
from collections import defaultdict
import threading
from .entities import EntityMatch  # Import from dedicated entities module


class EntityMapper: # class for mapping entities to placeholders
    """Maintains consistent entity mappings across document chunks with thread-safety."""
    
    def __init__(self): # constructor for entity mapper that will connect entities to placeholders
        self.entity_to_placeholder: Dict[EntityMatch, str] = {} # makes dictionary for holding entity as key and placeholder as value
        self.placeholder_to_entity: Dict[str, str] = {} # makes dictionary for holding placeholder as key and entity text as value
        self.counters: Dict[str, int] = defaultdict(int)    # makes counter for each entity label
        self._lock = threading.Lock()  # Thread-safe lock for concurrent access

    def get_or_create_placeholder(self, entity: EntityMatch) -> str: # function that will return existing placeholder or create new one for new entity
        """Get existing placeholder or create new one for entity (thread-safe)."""
        
        with self._lock:  # Ensure thread-safe access to shared state
            if entity in self.entity_to_placeholder:       # if the entity already has a placeholder (uses EntityMatch.__hash__)
                return self.entity_to_placeholder[entity]  # give it the same placeholder
            self.counters[entity.label] += 1    # if the entity is new, increase the counter for its label
            placeholder = f"[{entity.label}_{self.counters[entity.label]}]" # personalized label and entity are stored in placeholder

            self.entity_to_placeholder[entity] = placeholder # create a mapping entity to placeholder
            self.placeholder_to_entity[placeholder] = entity.text # create a mapping placeholder to entity text
            
            return placeholder # return the newly created placeholder
    
    def get_mapping(self) -> Dict[str, str]: # function for deanonymization
        """Get the complete placeholder to entity mapping (thread-safe)."""
        with self._lock:  # Ensure consistent snapshot of mappings
            return self.placeholder_to_entity.copy()    

