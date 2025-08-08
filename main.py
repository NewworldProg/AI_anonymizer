import time # time tracking
from time import sleep # simulate loading time
import os   # file operations
import tracemalloc # system resource tracking
from components import (    # components that contain the main functionality
    InputTextHandler,
    EntityDetector, 
    EntityMapper, 
    StatisticsGenerator, 
    TextDeanonymizer
)

def run_main():
    """Main anonymization workflow function."""
    print("Text Anonymization System")
    print("=" * 50)

    # Choose input text
    text = InputTextHandler().text_handler()
    print("\n" + "=" * 50)

    # Memory & time tracking
    tracemalloc.start()
    start_time = time.time()

    # Initialize components
    print("Initializing components...")
    entity_detector = EntityDetector("Jean-Baptiste/roberta-large-ner-english", confidence_threshold=0.8)
    entity_mapper = EntityMapper()
    statistics_generator = StatisticsGenerator()

    init_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()

    print(f"System initialized in {init_time:.2f}s, peak memory: {peak / 1024 / 1024:.1f} MB")
    print("===Initialization complete.===\n")
    input("⏸️ Press Enter to start chunk processing...\n")

    print("\n" + "=" * 50)
    print("Starting chunk processing...")

    # Chunking & processing
    chunk_start = time.time()
    all_entities = entity_detector.detect_entities_full_text(text)
    processing_time = time.time() - chunk_start
    current, peak = tracemalloc.get_traced_memory()

    print(f"Processing completed in {processing_time:.2f}s")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    print("\nAnonymization complete!")

    input("⏸️  Press Enter to show anonymized text preview...\n")
    print(f"\nAnonymized text preview:")
    from components.anonymizer import Anonymizer
    anonymizer = Anonymizer(text, all_entities, entity_mapper)
    anonymizer.anonymize()
    result_text = anonymizer.result_text
    text_preview = result_text[:400] + ("..." if len(result_text) > 400 else "")
    print(text_preview)
    # output preview of anonymized text

    input("⏸️  Press Enter to generate statistics...\n")

    print("\nGenerating statistics...")
    statistics = statistics_generator.generate_statistics(all_entities, entity_mapper.get_mapping())
    print(f"Found {statistics['total_entities']} entities")
    print(f"Processing time: {processing_time:.2f}s")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
    print("\nStatistics generation complete!")
    print("Confidence statistics by category:")
    for category, stats in statistics['confidence_stats'].items():
        print(f"  {category}: average confidence={stats['average confidence']:.3f}, min confidence={stats['min confidence']:.3f}, max confidence={stats['max confidence']:.3f}")

    print(f"Entity types found: {', '.join(statistics['entity_types_found'])}")

    # Save results
    save_choice = input("⏸️  Do you want to save the results? (y/n): ").strip().lower()
    if save_choice not in ['y', 'yes']:
        print("Skipping save. Exiting process.")
        exit(0)
    else:
        print("\nSaving results to output directory...")
        import os
        os.makedirs("output", exist_ok=True)

        with open("output/anonymized_text.txt", 'w', encoding='utf-8') as f:
            f.write(result_text)

        with open("output/original_text.txt", 'w', encoding='utf-8') as f:
            f.write(text)

        with open("output/entity_mappings.txt", 'w', encoding='utf-8') as f:
            f.write("ENTITY MAPPINGS\n" + "=" * 50 + "\n\n")
            for placeholder, original in entity_mapper.get_mapping().items():
                f.write(f"{placeholder} → '{original}'\n")

        with open("output/statistics.txt", 'w', encoding='utf-8') as f:
            f.write("ANONYMIZATION STATISTICS\n" + "=" * 50 + "\n\n")
            f.write(f"Total entities found: {statistics['total_entities']}\n")
            f.write(f"Unique entities: {statistics['unique_entities']}\n")
            f.write(f"Processing time: {processing_time:.2f}s\n")
            f.write(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB\n\n")
            f.write("Entity categories:\n")
            for category, count in statistics['by_category'].items():
                f.write(f"  {category}: {count}\n")
            f.write("\nConfidence statistics by category:\n")
            for category, stats in statistics['confidence_stats'].items():
                f.write(f"  {category}: average confidence={stats['average confidence']:.3f}, min confidence={stats['min confidence']:.3f}, max confidence={stats['max confidence']:.3f}\n")
            f.write(f"\nEntity types found: {', '.join(statistics['entity_types_found'])}\n")

        print("✅ Saved all outputs in /output")

    print("\n" + "=" * 50)
    deanon_choice = input("Test de-anonymization? (y/n): ").lower().strip()
    
    # input anonymized text and entity mapping
    if deanon_choice in ['y', 'yes']:
        print("Starting de-anonymization...")
        deanonymized = TextDeanonymizer.deanonymize_text(result_text, entity_mapper.get_mapping())
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

    print("\nProcess finished!")

if __name__ == "__main__":
    run_main()
