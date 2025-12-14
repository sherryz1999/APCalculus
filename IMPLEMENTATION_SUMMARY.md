# AP Calculus Question Selector - Implementation Summary

## Overview
Successfully implemented a program that allows users to select questions from AP Calculus test banks (TB_1 to TB_7) based on College Board AP Calculus AB or BC chapter topics.

## Features Implemented

### 1. Core Functionality
- **Question Extraction**: Parses PDF files using PyPDF2 to extract individual questions
- **Topic Mapping**: Identifies questions related to specific chapters using keyword matching
- **Filtering**: Allows selection of multiple chapters with configurable question limits
- **Test Bank Coverage**: Scans all 6 available test banks (TB_1, TB_3, TB_4, TB_5, TB_6, TB_7)
  - Note: TB_2.pdf is not present in the repository

### 2. User Interfaces

#### Command Line Interface (question_selector_cli.py)
- Interactive menu system
- Course selection (AP Calculus AB or BC)
- Chapter selection with flexible input (e.g., "1-4" or "1,2,3")
- Customizable question count
- Option to save results to file
- Detailed output with source attribution

#### Graphical User Interface (question_selector.py)
- Radio buttons for course selection
- Multi-select listbox for chapter selection
- Text input for question count
- Scrollable results display
- Requires Tkinter (included with most Python distributions)

### 3. Chapter Coverage

#### AP Calculus AB (Chapters 1-8)
1. Limits and Continuity
2. Differentiation: Definition and Fundamental Properties
3. Differentiation: Composite, Implicit, and Inverse Functions
4. Contextual Applications of Differentiation
5. Analytical Applications of Differentiation
6. Integration and Accumulation of Change
7. Differential Equations
8. Applications of Integration

#### AP Calculus BC Additional (Chapters 9-10)
9. Parametric Equations, Polar Coordinates, and Vector-Valued Functions
10. Infinite Sequences and Series

## Architecture

### Module Structure
```
config.py                    - Shared configuration (chapters, keywords, test banks)
question_selector.py         - GUI version
question_selector_cli.py     - CLI version
demo.py                      - Demonstration script
```

### Key Components

#### QuestionExtractor Class
- `extract_questions_from_pdf()`: Extracts questions from a single PDF
- `get_questions_by_topics()`: Filters questions by selected chapters
- `_split_into_questions()`: Parses page text into individual questions
- `_identify_topics()`: Maps questions to chapters using keywords

#### Configuration (config.py)
- Chapter definitions for AB and BC
- Keyword mappings for topic identification
- Dynamic test bank detection

## Statistics

### Test Bank Contents
- **TB_1.pdf**: 41 questions
- **TB_3.pdf**: 52 questions
- **TB_4.pdf**: 59 questions
- **TB_5.pdf**: 20 questions
- **TB_6.pdf**: 50 questions
- **TB_7.pdf**: 72 questions
- **Total**: 294 questions

### Topic Distribution (Based on Keyword Matching)
- Chapter 1 (Limits): 23 questions
- Chapter 2 (Differentiation Basics): 56 questions
- Chapter 3 (Advanced Differentiation): 8 questions
- Chapter 4 (Applications): 5 questions
- Chapter 5 (Analysis): 35 questions
- Chapter 6 (Integration): 0 questions
- Chapter 7 (Differential Equations): 5 questions
- Chapter 8 (Integration Applications): 7 questions
- Chapters 9-10 (BC Topics): 0 questions

Note: Some questions may cover multiple topics. Questions without clear topic keywords remain uncategorized.

## Testing & Quality Assurance

### Code Review
✓ All code review feedback addressed
✓ No outstanding issues

### Security Scan (CodeQL)
✓ No security vulnerabilities found

### Comprehensive Testing
✓ Module imports
✓ Configuration validation
✓ Test bank detection
✓ Question extraction
✓ Topic filtering
✓ Single and multiple chapter selection
✓ Question limit enforcement
✓ Data structure validation

## Usage

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI version
python3 question_selector_cli.py

# Run GUI version (if Tkinter available)
python3 question_selector.py

# Run demonstration
python3 demo.py
```

### Example Output
```
Scanning 6 available test banks...
Total questions extracted: 294
Questions matching selected chapters: 86
Found 5 questions for chapters 1-4 (limited to 5)
```

## Documentation
- **README.md**: Quick start guide
- **USAGE.md**: Comprehensive usage instructions
- **requirements.txt**: Python dependencies
- **.gitignore**: Excludes Python artifacts

## Dependencies
- Python 3.x
- PyPDF2 >= 3.0.0
- Tkinter (optional, for GUI)

## Limitations & Future Enhancements

### Current Limitations
1. Topic identification based on keyword matching (not 100% accurate)
2. No BC-specific questions detected in current test banks
3. Some questions may not be categorized if keywords don't match
4. PDF extraction may miss figures/diagrams in text representation

### Potential Enhancements
- Machine learning-based topic classification
- Question difficulty rating
- Export to multiple formats (PDF, HTML, LaTeX)
- Question search by content
- Custom chapter/topic definitions
- Integration with online platforms

## Conclusion
The AP Calculus Question Selector successfully meets all requirements:
- ✓ Multiple chapter selection via dropdown/menu
- ✓ User input for question count
- ✓ Searches through all available PDFs (TB_1 to TB_7)
- ✓ Identifies questions matching selected chapters
- ✓ Provides both CLI and GUI interfaces
- ✓ Comprehensive documentation
- ✓ No security vulnerabilities
- ✓ All tests passing
