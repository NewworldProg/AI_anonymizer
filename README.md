# Anonymisation_AI

## How to Run

1. Create a virtual environment and install requirements from `requirements.txt`.
2. Start the program by running `main.py` from the project root:
   ```
   python main.py
   ```
   This will guide you through the workflow and display process information.

## Program Overview

This program:
- Takes input as a text file (or manual/custom input).
- Outputs anonymized text, statistics about detected entities, and offers the option to deanonymize the text.

`main.py` orchestrates all components, each with defined inputs and outputs. Components are located in the `components/` folder.

---

## Component Breakdown

### 1. `input_text.py`
**Input:**  
- User selection (sample text, custom text, or file path).

**Output:**  
- Raw text string for further processing.

---

### 2. `chunk_processor.py`
**Input:**  
- Raw text from `input_text.py`.

**Output:**  
- Chunked text segments optimized for:
  - AI model (token-based chunking)
  - Regex model (pattern-aware chunking)

---

### 3. `entity_detector.py` --> AI_model and Regex
**Input:**  
- Chunked text segments from `chunk_processor.py`.

**Output:**  
- List of detected entities (`EntityMatch` objects), stored in an entity database.

---

### 4. `entities.py`
**Input:**  
- Data from `entity_detector.py`.

**Output:**  
- Data structures (`EntityMatch`, etc.) used by other components to represent detected entities.

---

### 5. `entity_mapper.py`
**Input:**  
- List of entities (`EntityMatch`).

**Output:**  
- Mapping of entities to unique placeholders (labels), used for:
  - Text anonymization
  - Deanonymization
  - Statistics generation

---

### 6. `anonymizer.py`
**Input:**  
- Raw text
- Entity-to-placeholder mapping

**Output:**  
- Anonymized text (entities replaced by placeholders)

---

### 7. `deanonymizer.py`
**Input:**  
- Anonymized text
- Placeholder-to-entity mapping

**Output:**  
- Restored original text

---

### 8. `statistics_generator.py`
**Input:**  
- List of entities
- Entity mapping

**Output:**  
- Statistics about detected entities (counts, categories, etc.)

---

## Workflow Summary

1. Text input
2. Text chunking
3. Entity detection
4. Entity mapping
5. Text anonymization
6. Statistics generation
7. Optional deanonymization

---