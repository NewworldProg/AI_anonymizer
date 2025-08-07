from components.entity_mapper import EntityMapper
from components.entities import EntityMatch

# input text, entities, and mapper
class Anonymizer:
    def __init__(self, text: str, entities: list[EntityMatch], mapper: EntityMapper):
        self.text = text
        self.entities = entities
        self.mapper = mapper
        self.supported_labels = {'PER', 'ORG', 'LOC', 'EMAIL', 'PHONE', 'MISC'}
        self.result_text = None
        self.filtered_entities = None

    def anonymize(self):
        valid_entities = [e for e in self.entities if e.label in self.supported_labels] # gets entites for labels
        result_text = self.text
        for entity in sorted(valid_entities, key=lambda e: e.start, reverse=True):
            placeholder = self.mapper.get_or_create_placeholder(entity)
            result_text = result_text[:entity.start] + placeholder + result_text[entity.end:]
        self.result_text = result_text
        self.filtered_entities = valid_entities

# output anonymized text with entities replaced by placeholders