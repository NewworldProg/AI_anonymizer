from typing import Dict
import re


class TextDeanonymizer:
    """Class for reversing the anonymization process with collision-safe replacement."""

    # input anonymized text and entity mapping
    @staticmethod
    def deanonymize_text(anonymized_text: str,  
                        entity_mapping: Dict[str, str]) -> str: 
        result = anonymized_text
        
        # Filter to only well-formed placeholders (start with [ and end with ])
        valid_placeholders = {k: v for k, v in entity_mapping.items() 
                            if k.startswith('[') and k.endswith(']')}
        
        # Sort placeholders by length (longest first) to avoid partial replacements
        sorted_placeholders = sorted(valid_placeholders.keys(), key=len, reverse=True)

        # Use precise replacement to avoid replacing parts of other placeholders or text
        for placeholder in sorted_placeholders:
            original_entity = valid_placeholders[placeholder]
            # Use word boundary regex to ensure exact match only
            escaped_placeholder = re.escape(placeholder)
            result = re.sub(escaped_placeholder, original_entity, result)
        
        return result