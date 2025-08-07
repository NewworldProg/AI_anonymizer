from typing import Dict    


class TextDeanonymizer:
    """Class for reversing the anonymization process."""
    
    @staticmethod
    def deanonymize_text(anonymized_text: str,  # function to reverse the anonymization process
                        entity_mapping: Dict[str, str]) -> str: # find placeholders and replace them with original entities
        """
        Reverse the anonymization process.
        
        Args:
            anonymized_text: Text with placeholders
            entity_mapping: Mapping from placeholders to original entities
            
        Returns:
            Original text with entities restored
        """
        result = anonymized_text
        
        # Filter to only well-formed placeholders (start with [ and end with ])
        valid_placeholders = {k: v for k, v in entity_mapping.items() 
                            if k.startswith('[') and k.endswith(']')}
        
        # Sort placeholders by length (longest first) to avoid partial replacements
        sorted_placeholders = sorted(valid_placeholders.keys(), key=len, reverse=True)
        
        for placeholder in sorted_placeholders:
            original_entity = valid_placeholders[placeholder]
            result = result.replace(placeholder, original_entity)
        
        return result