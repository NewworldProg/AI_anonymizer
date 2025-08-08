from typing import List, Dict, Any
from .entities import EntityMatch
from collections import Counter
class StatisticsGenerator: # class for generating statistics about anonymization process
    """Generates detailed statistics about anonymization process."""
    
    @staticmethod # static method that does not require instance of the class to be called
    def generate_statistics(entities: List[EntityMatch],  # function that will generate statistics, inputs = entities as key and list of entities that are same as value
                          entity_mapping: Dict[str, str]) -> Dict[str, Any]: # also makes a dicionary for dictionary with 2 string, all of that will be append to a dictionary
        """Generate comprehensive statistics."""
        by_category = Counter(entity.label for entity in entities) # count entities by their labels
        
        confidence_stats = {} # dictionary for holding confidence statistics
        for label in by_category.keys(): # iterate over each label found in the entities
            label_entities = [e for e in entities if e.label == label] # filter entities by label
            confidences = [e.confidence for e in label_entities] # extract confidence scores
            confidence_stats[label] = {
                'average confidence': sum(confidences) / len(confidences),
                'min confidence': min(confidences),
                'max confidence': max(confidences)
            }
        
        return {
            'total_entities': len(entities),
            'unique_entities': len(entity_mapping),  # Number of unique mapped entities
            'by_category': dict(by_category),
            'confidence_stats': confidence_stats,
            'entity_types_found': list(by_category.keys())
        }
