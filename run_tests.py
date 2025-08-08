#!/usr/bin/env python3
"""
Test runner script for AI_anonymizer project.
Runs all tests in the tests/ directory using pytest.
"""

import pytest
import sys
import os
from pathlib import Path

def main():
    """Run all tests in the project."""
    # Get the project root directory (where this script is located)
    project_root = Path(__file__).parent
    
    # Add project root to Python path so imports work correctly
    sys.path.insert(0, str(project_root))
    
    # Define test directory
    test_dir = project_root / "tests"
    
    if not test_dir.exists():
        print(f"❌ Test directory '{test_dir}' not found!")
        return 1
    
    print("Running AI_anonymizer test suite...")
    print(f"Test directory: {test_dir}")
    print("=" * 60)
    
    # Configure pytest arguments
    pytest_args = [
        str(test_dir),           # Run tests in tests/ directory
        "-v",                    # Verbose output
        "--tb=short",           # Short traceback format
        "--color=yes",          # Colored output
        "-x",                   # Stop on first failure (optional)
        "--durations=10",       # Show 10 slowest tests
    ]
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
