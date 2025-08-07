from components.entity_mapper import EntityMapper
from components.entity_detector import EntityDetector
from components.entities import EntityMatch, AnonymizationResult

class Anonymizer:
    def __init__(self, text: str, entities: list, mapper):
        self.text = text
        self.entities = entities
        self.mapper = mapper
        self.entity_types = ['PER', 'ORG', 'LOC', 'EMAIL', 'PHONE', 'MISC']
        
        # Odmah obavi zamenu pri kreiranju instance
        self.result_text, self.filtered_entities = self._anonymize()
    
    def _anonymize(self):
        filtered = [e for e in self.entities if e.label in self.entity_types]
        result_text = self.text
        for entity in sorted(filtered, key=lambda x: x.start, reverse=True):
            placeholder = self.mapper.get_or_create_placeholder(entity)
            result_text = result_text[:entity.start] + placeholder + result_text[entity.end:]
        return result_text, filtered

