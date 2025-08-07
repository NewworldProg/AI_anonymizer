import re 
import logging
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from .entities import EntityMatch
from .chunk_processor import ChunkProcessor
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EntityDetector:
    """Handles entity detection using transformer models and regex patterns."""
    # model default parameters
    def __init__(self, model_name: str = "Jean-Baptiste/roberta-large-ner-english", 
                 confidence_threshold: float = 0.8):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.chunk_processor = ChunkProcessor()
        
        self._setup_model()
        self._setup_patterns()
    
    def _setup_model(self): # setting up the model
        try:
            torch.set_num_threads(2)  # Limit CPU threads
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name) 
            self.model = AutoModelForTokenClassification.from_pretrained(self.model_name) 
            self.ner_pipeline = pipeline(
                "ner", # task type
                model=self.model,
                tokenizer=self.tokenizer, 
                aggregation_strategy="simple", 
                device=-1,  # Force CPU
                torch_dtype=torch.float32 # use basic float32 for precision
            )
            logger.info(f"Loaded NER model: {self.model_name}") # log that its loaded
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise
    
    def _setup_patterns(self): # setting up regex patterns
        """Setup regex patterns for additional entity types.""" 
        try:
            self.patterns = {
                'EMAIL': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
                'PHONE': re.compile(r'\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|'
                                r'\b1-800-[A-Z]{7}\b'),
                'URL': re.compile(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?)?')
            }
            logger.info("Loaded regex patterns for EMAIL, PHONE, and URL detection")
        except Exception as e:
            logger.error(f"Failed to setup regex patterns: {e}")
            raise
    
    def detect_entities_full_text(self, text: str) -> List[EntityMatch]: 
        """
        Advanced detection with precise offset mapping:
        - Tokenized chunking for NER (uses offset_mapping for exact positions)
        - Pattern-aware chunking for regex (avoids breaking patterns)
        """
        if not text or not text.strip():
            return []
        
        entities = []
        
        # logging regex detection with pattern-aware chunking
        logger.info("Phase 1/2: Regex detection with pattern-aware chunking...")
        entities.extend(self._detect_entities_regex_chunked(text))

        # logging NER detection on tokenized chunks
        logger.info("Phase 2/2: NER detection with precise tokenized chunking...")
        entities.extend(self._detect_entities_ner_chunked(text))
        
        logger.info(f"Raw entities found: {len(entities)}")
        logger.info("Deduplicating entities...")
        deduplicated = self._deduplicate_entities(entities)
        logger.info(f"Final entities after deduplication: {len(deduplicated)}")
        
        return deduplicated

    def _detect_entities_ner_chunked(self, text: str) -> List[EntityMatch]:
        """NER detection with tokenized chunking for optimal transformer performance."""
        # Use ChunkProcessor for tokenized chunking
        chunks = self.chunk_processor.create_tokenized_chunks(text, self.tokenizer, max_tokens=400, overlap_tokens=25)
        
        entities = []
        total_chunks = len(chunks)
        
        for i, (chunk_text, chunk_offset) in enumerate(chunks, 1): # chunked text and starting position in specific chunk
            logger.info(f"Processing NER chunk {i}/{total_chunks} (offset: {chunk_offset})")
            ner_entities = self._detect_entities_ner(chunk_text, chunk_offset)
            entities.extend(ner_entities) # extend the list with new entities
            logger.info(f"Found {len(ner_entities)} entities in chunk {i}")
        
        logger.info(f"NER processing complete: {len(entities)} total entities from {total_chunks} chunks")
        return entities

    def _detect_entities_regex_chunked(self, text: str) -> List[EntityMatch]: 
        """Regex detection with character-based chunking that respects pattern boundaries."""
        chunks = self.chunk_processor.create_regex_safe_chunks(text, chunk_size=5000, overlap_size=200) # chunk logic in chunk_processor
        
        entities = []
        total_chunks = len(chunks)
        
        for i, (chunk_text, chunk_offset) in enumerate(chunks, 1): # chunked text and starting position in specific chunk
            logger.info(f"Processing regex chunk {i}/{total_chunks} (offset: {chunk_offset})")
            regex_entities = self._detect_entities_regex(chunk_text, chunk_offset)
            entities.extend(regex_entities)
            logger.info(f"Found {len(regex_entities)} regex entities in chunk {i}")
        
        logger.info(f"Regex processing complete: {len(entities)} total entities from {total_chunks} chunks")
        return entities

    def _detect_entities_ner(self, text: str, chunk_offset: int = 0) -> List[EntityMatch]:
        """Detect entities using NER model."""
        entities = []
        # input text chunk
        try:
            ner_results = self.ner_pipeline(text) # result of text processing through NER pipeline
            for entity in ner_results: # iterate through NER results
                if entity['score'] >= self.confidence_threshold: # confidence score
                    label = self._map_label(entity['entity_group']) # NER labels
                    start_pos = entity['start'] + chunk_offset  # start position adjusted for chunking
                    end_pos = entity['end'] + chunk_offset  # end position adjusted for chunking
                    
                    # Use exact text from original source instead of entity['word']
                    # This preserves exact spacing and avoids tokenizer artifacts
                    actual_text = text[entity['start']:entity['end']]
                    
                    if actual_text and actual_text.strip():  # Only check if not empty after stripping
                        entities.append(EntityMatch(
                            text=actual_text,
                            label=label,
                            start=start_pos,
                            end=end_pos,
                            confidence=entity['score']
                        ))
        except Exception as e:
            logger.warning(f"NER model detection failed: {e}")
        # output entities
        return entities

    def _detect_entities_regex(self, text: str, chunk_offset: int = 0) -> List[EntityMatch]:
        """Detect entities using regex patterns."""
        entities = []
        #input text chunk
        for label, pattern in self.patterns.items(): # loads regex patterns
            for match in pattern.finditer(text): # find all matches in text
                entity_text = match.group()
                if entity_text.strip():  # Only check if not empty
                    entities.append(EntityMatch(
                        text=entity_text,
                        label=label,
                        start=match.start() + chunk_offset,
                        end=match.end() + chunk_offset,
                        confidence=1.0
                    ))
        # output entities
        return entities

    def _deduplicate_entities(self, entities: List[EntityMatch]) -> List[EntityMatch]:
        """Remove duplicate and overlapping entities (improved for chunking)."""
        # input entities from EntityMatch
        if not entities: # check if entities list is empty
            return entities
        
        # Step 1: Remove exact positional duplicates (same entity found multiple times at same position)
        # This handles chunking overlap where the same entity appears in multiple chunks
        seen_positions = set()
        position_deduplicated = []
        exact_duplicate_count = 0
        # iterate through entities from EntityMatch
        for entity in entities:
            # Use position + text + label as key for exact duplicates
            key = (entity.start, entity.end, entity.text.lower(), entity.label)
            if key not in seen_positions:
                seen_positions.add(key)
                position_deduplicated.append(entity)
                #output unique entity with start, end, text and label
            else:
                exact_duplicate_count += 1


        # Step 2: Handle overlapping entities (keep highest confidence)
        # Sort by start position, then by confidence (highest first)
        position_deduplicated.sort(key=lambda x: (x.start, -x.confidence)) # sort first by earlier start position and more confidence
        final_entities = []
        overlap_removed_count = 0
        # input position_deduplicated from previous step
        for entity in position_deduplicated: # iterate through deduplicated entities
            overlaps = False
            for existing in final_entities: # finding overals
                if (entity.start < existing.end and entity.end > existing.start): # Check for overlap
                    if entity.confidence > existing.confidence: # If current entity has higher confidence
                        final_entities.remove(existing) # Remove existing
                        overlap_removed_count += 1
                        break
                    else:
                        overlaps = True # If existing entity has higher confidence
                        overlap_removed_count += 1
                        break # do nothing, skip adding current entity

            if not overlaps: # If no overlap, add
                final_entities.append(entity)
        # output deduplicated entities
        logger.info(f"Deduplication: Removed {exact_duplicate_count} exact duplicates.")
        logger.info(f"Deduplication: Removed {overlap_removed_count} overlapping entities (lower confidence).")
        return final_entities
    
    def _map_label(self, model_label: str) -> str:
        """Map model-specific labels to standard labels."""
        label_mapping = {
            'PERSON': 'PER',
            'ORGANIZATION': 'ORG',
            'LOCATION': 'LOC',
            'MISCELLANEOUS': 'MISC'
        }
        return label_mapping.get(model_label, model_label)

   