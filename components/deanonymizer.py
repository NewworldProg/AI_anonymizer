from typing import Dict    


class TextDeanonymizer:
    """Class for reversing the anonymization process."""

    # input anonymized text and entity mapping
    @staticmethod
    def deanonymize_text(anonymized_text: str,  
                        entity_mapping: Dict[str, str]) -> str: 
        result = anonymized_text
        
        # Filter to only well-formed placeholders (start with [ and end with ])
        valid_placeholders = {k: v for k, v in entity_mapping.items() 
                            if k.startswith('[') and k.endswith(']')}
        
        # Sort placeholders by length (longest first) 
        sorted_placeholders = sorted(valid_placeholders.keys(), key=len, reverse=True)

        # takes placeholders from entity mapping and replaces them in the text
        for placeholder in sorted_placeholders:
            original_entity = valid_placeholders[placeholder]
            result = result.replace(placeholder, original_entity)
        
        return result