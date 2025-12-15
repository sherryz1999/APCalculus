# AP Calculus Question Selector

This program allows you to select a subset of questions from AP Calculus test banks (TB_1 to TB_7) matching specific College Board AP Calculus AB or BC chapters.

## Features

- Select from AP Calculus AB (Chapters 1-8) or BC (Chapters 1-10)
- Choose multiple chapters using individual selections or ranges
- Specify the number of questions to retrieve
- Search through all test bank PDFs (TB_1.pdf through TB_7.pdf)
- View results on screen or save to a file
- Both GUI and CLI versions available

## Requirements

- Python 3.x
- PyPDF2 library

## Installation

1. Install the required library:
```bash
pip install PyPDF2
```

2. For the GUI version (if available in your environment):
```bash
pip install tkinter  # May already be included with Python
```

## Usage

### Command Line Interface (CLI)

Run the CLI version:
```bash
python3 question_selector_cli.py
```

Follow the interactive prompts:
1. Select course (AP Calculus AB or BC)
2. View available chapters
3. Select chapters (e.g., "1,2,3" or "1-4")
4. Enter number of questions (0 for all matching questions)
5. View results and optionally save to a file

Example session:
```
AP CALCULUS QUESTION SELECTOR
================================================================================

Select Course:
1. AP Calculus AB
2. AP Calculus BC

Enter choice (1 or 2): 1

Available Chapters for AP Calculus AB:
--------------------------------------------------------------------------------
  1. Limits and Continuity
  2. Differentiation: Definition and Fundamental Properties
  3. Differentiation: Composite, Implicit, and Inverse Functions
  4. Contextual Applications of Differentiation
  ...

Select Chapters:
Enter chapter numbers separated by commas (e.g., 1,2,3)
Or enter a range (e.g., 1-4)

Your selection: 1-4

Number of Questions:
Enter the number of questions to retrieve (0 for all): 10
```

### Graphical User Interface (GUI)

Run the GUI version (requires Tkinter):
```bash
python3 question_selector.py
```

The GUI provides:
- Radio buttons to select AP Calculus AB or BC
- Multi-select listbox for chapter selection
- Text input for number of questions
- "Search Questions" button to find matching questions
- Scrollable text area to view results

## AP Calculus Chapter Topics

### AP Calculus AB (Chapters 1-8)
1. Limits and Continuity
2. Differentiation: Definition and Fundamental Properties
3. Differentiation: Composite, Implicit, and Inverse Functions
4. Contextual Applications of Differentiation
5. Analytical Applications of Differentiation
6. Integration and Accumulation of Change
7. Differential Equations
8. Applications of Integration

### AP Calculus BC Additional Topics (Chapters 9-10)
9. Parametric Equations, Polar Coordinates, and Vector-Valued Functions
10. Infinite Sequences and Series

## How It Works

The program:
1. Scans all PDF test banks (TB_1.pdf through TB_7.pdf)
2. Extracts individual questions from each page
3. Identifies topics based on keyword matching
4. Filters questions that match your selected chapters
5. Returns up to the requested number of questions

## Output Format

For each matching question, the program displays:
- Question number
- Source PDF file and page number
- Associated chapter/topic numbers
- Full question text

## Saving Results

When using the CLI, you can save search results to a text file for future reference. The default filename is `selected_questions.txt`, but you can specify a custom name.

## Notes

- The topic identification uses keyword matching, which may not be 100% accurate
- Some questions may cover multiple topics and will be tagged accordingly
- Questions without clear topic keywords may not be categorized
- The program searches through approximately 300+ questions across all test banks

## Troubleshooting

**Problem**: "No module named 'PyPDF2'"
**Solution**: Install PyPDF2 using `pip install PyPDF2`

**Problem**: "No questions found matching the selected criteria"
**Solution**: Try selecting more chapters or set the question count to 0 to see all matching questions

**Problem**: PDF reading errors
**Solution**: Ensure all TB_*.pdf files are in the same directory as the Python scripts

## License

This tool is for educational purposes to help students practice AP Calculus problems.
