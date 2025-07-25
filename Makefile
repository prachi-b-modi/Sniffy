.PHONY: all test test-verbose clean help

all: test

test:
	python -m unittest discover tests -v

test-verbose:
	python run_tests.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.tmp" -delete

help:
	@echo "Available targets:"
	@echo "  test        - Run all tests using unittest"
	@echo "  test-verbose - Run tests with verbose output"  
	@echo "  clean       - Remove Python cache files"
	@echo "  help        - Show this help message"