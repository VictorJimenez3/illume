# Illume

Illume is an AI-powered learning assistant designed to help students understand complex topics during research. It leverages advanced language models to provide clear, contextual explanations and insights.

## Features

- AI-powered learning assistance
- Complex topic explanation
- Research support
- Interactive learning experience

## Project Overview

Illume is structured to provide an intuitive and powerful learning experience:

### Core Components
The project implements a focused RAG (Retrieval-Augmented Generation) architecture:

#### 1. LLM Engineering (`llm_engineering/`)
The core module that handles AI interactions through Google's Gemini model:

- **Model Interface**
  - `models/gemini_client.py`: Manages Google Gemini API interactions
  - Handles connection lifecycle and resource cleanup
  - Implements text generation capabilities

- **Core Operations** (`models/operations.py`)
  - `create_word_explanation(keyword: str, data: str) -> str`: Generates contextual word definitions
  - `create_questions(keyword: str, text: str) -> str`: Generates relevant assessment questions
  - `create_answers(questions: str) -> str`: Produces detailed answers with explanations
  - `create_initial_summary(data: str) -> str`: Summarizes input context
  - `create_new_questions(wrong_questions: str, keyword: str, text: str) -> str`: Generates new questions based on incorrect answers
  - `create_summary_adjustment(keyword: str, new_questions: str, new_answers: str) -> str`: Creates an adjusted summary based on new Q&A
  - Each operation implements specific prompting strategies

- **Infrastructure Layer** (`infrastructure/`)
  - `clean_wiki_content()`: Preprocesses Wikipedia text data
  - Manages data loading and cleaning operations
  - Handles file I/O for test data

### Operation Functions Documentation

The following functions are available in `llm_engineering/models/operations.py`:

1. **create_initial_summary(data: str) -> str**
   - Purpose: Creates an initial summary of the provided data
   - Parameters:
     - `data`: The text content to summarize
   - Returns: A string containing the generated summary

2. **create_questions(keyword: str, text: str) -> str**
   - Purpose: Generates 4 assessment questions about a specific keyword
   - Parameters:
     - `keyword`: The topic to generate questions about
     - `text`: The context text to base questions on
   - Returns: A string containing 4 formatted questions (multiple choice, true/false, fill-in-blank)

3. **create_answers(questions: str) -> str**
   - Purpose: Generates answers and explanations for provided questions
   - Parameters:
     - `questions`: The questions to answer
   - Returns: A string containing answers and explanations for each question

4. **create_new_questions(wrong_questions: str, keyword: str, text: str) -> str**
   - Purpose: Generates new questions focusing on previously incorrect answers
   - Parameters:
     - `wrong_questions`: Questions that were answered incorrectly
     - `keyword`: The topic to focus on
     - `text`: The context text
   - Returns: A string containing 4 new questions focusing on reinforcement

5. **create_word_explanation(keyword: str, data: str) -> str**
   - Purpose: Creates a detailed explanation of a keyword in context
   - Parameters:
     - `keyword`: The word to explain
     - `data`: The article context
   - Returns: A string containing the word's meaning and contextual explanation

6. **create_summary_adjustment(keyword: str, new_questions: str, new_answers: str) -> str**
   - Purpose: Creates an adjusted explanation based on new Q&A
   - Parameters:
     - `keyword`: The topic being explained
     - `new_questions`: The new questions generated
     - `new_answers`: The answers to the new questions
   - Returns: A string containing the adjusted explanation

#### 2. Application Logic (`app/`)
- **PabloAI Class** (`actions.py`)
  - Orchestrates the RAG workflow
  - Implements error handling and logging
  - Manages the conversation flow:
    1. Data cleaning
    2. Word explanation generation
    3. Question generation
    4. Answer creation

### Software Engineering Principles

1. **Clean Architecture**
   - Clear separation between model operations and application logic
   - Infrastructure layer handles data processing independently
   - Modular design with well-defined responsibilities

2. **Error Handling**
   - Comprehensive try-except blocks in PabloAI
   - Graceful client cleanup in finally blocks
   - Clear error messaging for debugging

3. **Development Tools** (as defined in `pyproject.toml`)
   - pytest for testing
   - black for code formatting (line length standardization)
   - isort for import organization

### Example Usage
The `examples/` directory contains sample implementations showing how to use Illume:
- `runningPabloAI.py`: Demonstrates basic usage and integration
- Additional examples show different use cases and features

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Poetry for dependency management
- Google AI API access (for Google's Generative AI)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/illume.git
cd illume
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up your environment variables:
Create a `.env` file in the root directory with your Google AI API key:
```
GOOGLE_API_KEY=your_api_key_here
```

### Running the Example
```bash
poetry run python examples/runningPabloAI.py
```

## Development Guide

This section is intended for developers who will be working on or extending the Illume project.

### Project Structure
```
illume/
├── llm_engineering/     # Core implementation
├── examples/           # Usage examples
├── tests/             # Test suite
└── pyproject.toml     # Project configuration
```

### Development Setup
1. Follow the installation steps above
2. Install development dependencies:
```bash
poetry install --with dev
```

### Development Tools
The project uses several development tools to maintain code quality:
- `pytest`: For running tests
- `black`: For code formatting
- `isort`: For import sorting

### Code Style Guidelines
1. Follow PEP 8 standards
2. Use type hints for function parameters and return values
3. Write docstrings for all public functions and classes
4. Keep functions focused and single-purpose
5. Write unit tests for new features

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

## License

This project is licensed under the terms specified in the LICENSE file.

