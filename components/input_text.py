class InputTextHandler:
    def __init__(self, default_file_path=None):
        self.default_file_path = default_file_path
        self.last_loaded_text = None

    def text_handler(self) -> str:
        print("Input options:")
        print("1. Use sample text")
        print("2. Enter custom text")
        print("3. Load from file path")

        while True:
            choice = input("Choose option (1/2/3): ").strip()
            if choice == "1":
                text = """"Dear John Smith and Mary Johnson,
Thank you for your interest in our services at Acme Corporation. 
Please contact us at info@acme.com or call our office at 555-123-4567.
Our headquarters are located in New York City, with additional offices 
in San Francisco and London. We serve major clients including 
Microsoft, Google, and Amazon.
For technical support, reach out to support@acme.com or call 
1-800-SUPPORT. You can also visit our website at www.acme.com.
Best regards,
Robert Davis
CEO, Acme Corporation
robert.davis@acme.com
Direct: 555-987-6543"
                """
                print(f"Using sample text ({len(text)} characters)")
                self.last_loaded_text = text
                return text

            elif choice == "2":
                text = input("Enter your text: ")
                print(f"Using custom text ({len(text)} characters)")
                self.last_loaded_text = text
                return text

            elif choice == "3":
                file_path = self.default_file_path or input("Enter file path: ").strip()
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    print(f"Loaded text from '{file_path}' ({len(text)} characters)")
                    self.last_loaded_text = text
                    return text
                except FileNotFoundError:
                    print(f"❌ Error: File not found: {file_path}")
                except Exception as e:
                    print(f"❌ Error reading file: {e}")
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.\n")
