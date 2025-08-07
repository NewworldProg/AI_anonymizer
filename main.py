import time # time tracking
from time import sleep # simulate loading time
import os   # file operations
import psutil # system resource tracking
from components import (    # components that contain the main functionality
    InputTextHandler,
    EntityDetector, 
    EntityMapper, 
    StatisticsGenerator, 
    TextDeanonymizer
)

if __name__ == "__main__":
    
    print("Text Anonymization System")
    print("=" * 50)
    
    # Choose input text
    text = InputTextHandler().text_handler()



    print("\n" + "=" * 50)
    
    # input setting up tracking loading tracking resources
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.time()
    
    # input setting up program components
    print("Initializing components...")
    entity_detector = EntityDetector("Jean-Baptiste/roberta-large-ner-english", confidence_threshold=0.8)
    entity_mapper = EntityMapper()
    statistics_generator = StatisticsGenerator()
    init_time = time.time() - start_time
    init_memory = process.memory_info().rss / 1024 / 1024  # MB


    print(f"System initialized in {init_time:.2f}s, memory: {init_memory - start_memory:.1f} MB")
    print("===Initialization complete.===\n")
    input("⏸️ Press Enter to start chunk processing...\n")

    # input text
    print("\n" + "=" * 50)
    print("Starting chunk processing...")

    # track chunk processing
    chunk_start = time.time()
    # initialize chunking and processing    
    all_entities = entity_detector.detect_entities_full_text(text)
    processing_time = time.time() - chunk_start
    final_memory = process.memory_info().rss / 1024 / 1024  # MB

    print(f"Processing completed in {processing_time:.2f}s")
    print(f"Memory used: {final_memory - start_memory:.1f} MB")
    print(f"Peak memory usage: {final_memory:.1f} MB")
    print("\nAnonymization complete!")
    # output EntityMatch data filled for useage in anonymization/de-anonymization and statistics generation

    # input EntityMatch data filled for useage
    input("⏸️  Press Enter to show anonymized text preview...\n")
    print(f"\nAnonymized text preview:")
    from components.anonymizer import Anonymizer
    anonymizer = Anonymizer(text, all_entities, entity_mapper)
    result_text = anonymizer.result_text
    filtered_entities = anonymizer.filtered_entities
    text_preview = result_text[:200] + ("..." if len(result_text) > 200 else "")
    print(text_preview)
    # output preview of anonymized text

    input("⏸️  Press Enter to generate statistics...\n")
    
    # input EntityMatch data filled for useage
    # Generate statistics
    print("\nGenerating statistics...")
    statistics = statistics_generator.generate_statistics(filtered_entities, entity_mapper.get_mapping())
    print(f"Found {statistics['total_entities']} entities")
    print(f"Processing time: {processing_time:.2f}s")
    print(f"Memory used: {final_memory - start_memory:.1f} MB")
    print("\nStatistics generation complete!")
    # output generated statistics
    
    # Save option
    save_choice = input("⏸️  do you want to save the results? ""(y/n): ").strip().lower()
    if save_choice not in ['y', 'yes']:
        print("Skipping save. Exiting process.")
        exit(0)
    else:
        print("\nSaving results to output directory...")
        os.makedirs("output", exist_ok=True)
        
        # Save anonymized text
        with open("output/anonymized_text.txt", 'w', encoding='utf-8') as f:
            f.write(result_text)
        
        # Save original text
        with open("output/original_text.txt", 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save entity mappings
        with open("output/entity_mappings.txt", 'w', encoding='utf-8') as f:
            f.write("ENTITY MAPPINGS\n")
            f.write("=" * 50 + "\n\n")
            for placeholder, original in entity_mapper.get_mapping().items():
                f.write(f"{placeholder} → '{original}'\n")
        
        # Save statistics
        with open("output/statistics.txt", 'w', encoding='utf-8') as f:
            f.write("ANONYMIZATION STATISTICS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total entities found: {statistics['total_entities']}\n")
            f.write(f"Unique entities: {statistics['unique_entities']}\n")
            f.write(f"Processing time: {processing_time:.2f}s\n")
            f.write(f"Memory used: {final_memory - start_memory:.1f} MB\n\n")
            f.write("Entity categories:\n")
            for category, count in statistics['by_category'].items():
                f.write(f"  {category}: {count}\n")
        
        print("✅ Saved: output/anonymized_text.txt")
        print("✅ Saved: output/original_text.txt") 
        print("✅ Saved: output/entity_mappings.txt")
        print("✅ Saved: output/statistics.txt")
        print("\nResults saved successfully!")

    print("\n" + "=" * 50)
    # input EntityMatch data filled for useage
    # Ask for de-anonymization
    deanon_choice = input("Test de-anonymization? (y/n): ").lower().strip()
    if deanon_choice in ['y', 'yes']:
        print("Starting de-anonymization...")
        deanonymized = TextDeanonymizer.deanonymize_text(
            result_text, entity_mapper.get_mapping()
        )
        success = deanonymized == text
        print(f"De-anonymization {'successful' if success else 'failed'}")
        
        # Save deanonymized text
        with open("output/deanonymized_text.txt", 'w', encoding='utf-8') as f:
            f.write(deanonymized)
        
        if success:
            print("Original text fully restored!")
        else:
            print("Minor differences detected.")
    else:
        print("Skipping de-anonymization test.")
    # output de-anonymized text and results
    print("\nProcess finished!")
    