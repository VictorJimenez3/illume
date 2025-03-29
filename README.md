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
  - `create_word_explanation()`: Generates contextual word definitions
  - `create_questions()`: Generates relevant assessment questions
  - `create_answers()`: Produces detailed answers with explanations
  - `create_initial_summary()`: Summarizes input context
  - Each operation implements specific prompting strategies

- **Infrastructure Layer** (`infrastructure/`)
  - `clean_wiki_content()`: Preprocesses Wikipedia text data
  - Manages data loading and cleaning operations
  - Handles file I/O for test data

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

## Author

Pablo Leyva 

## Contact

- LinkedIn: [Pablo Leyva](https://www.linkedin.com/in/pablo-leyva/)
- AI Partner Solutions at Apple 
- Email: pleyva2004@gmail.com

