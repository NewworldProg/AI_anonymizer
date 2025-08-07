#!/usr/bin/env python3
"""
Optimized text chunking processor for anonymization system.
Supports multiple chunking strategies for different use cases.
"""

import re
import logging      # logging for debug info
from typing import List, Tuple

logger = logging.getLogger(__name__)

class ChunkProcessor:

    def __init__(self, chunk_size: int = None, overlap_size: int = None, **kwargs):
        """Constructor for chunk processor with optional chunk and overlap sizes."""
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
    
    def create_tokenized_chunks(self, text: str, tokenizer, max_tokens: int = 400, overlap_tokens: int = 25) -> List[Tuple[str, int]]:
        """Create chunks based on tokenizer boundaries with precise offset mapping."""
        if not text:
            return []
        
        # Use a more conservative token limit to avoid sequence length warnings
        # RoBERTa has a 512 token limit, so we use 400 for safety
        effective_max_tokens = min(max_tokens, 400)
        
        # Tokenize with offset mapping to get exact character positions
        tokenized = tokenizer(
            text, 
            add_special_tokens=False, 
            truncation=False, 
            return_offsets_mapping=True
        )
        
        tokens = tokenized['input_ids']
        offset_mapping = tokenized['offset_mapping']
        
        chunks = []
        start_token = 0
        
        while start_token < len(tokens):
            # Define end token for this chunk
            end_token = min(start_token + effective_max_tokens, len(tokens))
            
            # Get character start and end positions from offset mapping
            chunk_char_start = offset_mapping[start_token][0]
            chunk_char_end = offset_mapping[end_token - 1][1]
            
            # Extract the exact text using character positions
            chunk_text = text[chunk_char_start:chunk_char_end]
            chunk_offset = chunk_char_start
            
            chunks.append((chunk_text, chunk_offset))
            
            # Move to next chunk with overlap
            if end_token >= len(tokens):
                break
            start_token = end_token - min(overlap_tokens, effective_max_tokens // 4)
            
        logger.info(f"Created {len(chunks)} tokenized chunks for NER processing (max {effective_max_tokens} tokens each)")
        return chunks

    def create_regex_safe_chunks(self, text: str, chunk_size: int = 5000, overlap_size: int = 200) -> List[Tuple[str, int]]:
        """Create chunks that avoid breaking regex patterns at boundaries."""
        if not text or len(text) <= chunk_size:
            return [(text, 0)]
        
        chunks = []
        start = 0
        text_length = len(text)
        
        # Characters that commonly appear in patterns we want to preserve
        safe_break_chars = {' ', '\n', '\t', '.', '!', '?', ';', '\r'}
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            # If not at the end of text, try to find a safe break point
            if end < text_length:
                # Look for safe break characters near the intended end
                search_start = max(end - 50, start + chunk_size // 2)
                search_end = min(end + 50, text_length)
                
                best_break = end
                for i in range(search_end - 1, search_start - 1, -1):
                    if text[i] in safe_break_chars:
                        # Additional check: avoid breaking URLs, emails, phone numbers
                        if not self._is_inside_pattern(text, i):
                            best_break = i + 1
                            break
                
                end = best_break
            
            chunk = text[start:end]
            chunks.append((chunk, start))
            
            if end >= text_length:
                break
                
            start = end - overlap_size
            # Ensure no infinite loop
            if start <= chunks[-1][1]:
                start = chunks[-1][1] + 1
        
        logger.info(f"Created {len(chunks)} regex-safe chunks")
        return chunks

    def _is_inside_pattern(self, text: str, position: int) -> bool:
        """Check if position is inside a potential regex pattern."""
        # Check a small window around the position
        window_start = max(0, position - 30)
        window_end = min(len(text), position + 30)
        window = text[window_start:window_end]
        
        # Look for patterns that shouldn't be broken
        patterns_to_avoid = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email
            r'https?://[^\s]+',  # URL
            r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # Phone
        ]
        
        for pattern in patterns_to_avoid:
            for match in re.finditer(pattern, window):
                match_start = window_start + match.start()
                match_end = window_start + match.end()
                if match_start <= position <= match_end:
                    return True
        
        return False

