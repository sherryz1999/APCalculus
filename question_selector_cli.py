#!/usr/bin/env python3
"""
AP Calculus Question Selector - Command Line Interface

This program allows users to select a subset of questions from AP Calculus test banks
matching specific College Board AP Calculus AB or BC chapters via command line.
"""

import PyPDF2
import os
import re
from typing import List, Dict


# AP Calculus AB Chapter/Topic Mapping (Based on College Board Course Framework)
AP_CALCULUS_AB_CHAPTERS = {
    "1": "Limits and Continuity",
    "2": "Differentiation: Definition and Fundamental Properties",
    "3": "Differentiation: Composite, Implicit, and Inverse Functions",
    "4": "Contextual Applications of Differentiation",
    "5": "Analytical Applications of Differentiation",
    "6": "Integration and Accumulation of Change",
    "7": "Differential Equations",
    "8": "Applications of Integration"
}

# AP Calculus BC Additional Chapters (includes all AB + additional topics)
AP_CALCULUS_BC_ADDITIONAL = {
    "9": "Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
    "10": "Infinite Sequences and Series"
}

# Topic keywords for identifying questions (simplified mapping)
TOPIC_KEYWORDS = {
    "1": ["limit", "continuity", "asymptote", "discontinuity", "intermediate value"],
    "2": ["derivative", "rate of change", "tangent line", "differentiable", "power rule"],
    "3": ["chain rule", "implicit differentiation", "inverse function", "composite"],
    "4": ["related rates", "motion", "velocity", "acceleration", "optimization"],
    "5": ["mean value theorem", "critical point", "extrema", "increasing", "decreasing", "concavity", "inflection"],
    "6": ["integral", "antiderivative", "riemann sum", "accumulation", "fundamental theorem"],
    "7": ["differential equation", "slope field", "exponential growth", "separation of variables"],
    "8": ["area", "volume", "disk", "washer", "average value"],
    "9": ["parametric", "polar", "vector"],
    "10": ["series", "sequence", "convergence", "divergence", "taylor", "maclaurin"]
}


class QuestionExtractor:
    """Extracts questions from PDF test banks."""
    
    def __init__(self, pdf_dir: str = "."):
        self.pdf_dir = pdf_dir
        self.test_banks = [f"TB_{i}.pdf" for i in [1, 3, 4, 5, 6, 7]]
    
    def extract_questions_from_pdf(self, filename: str) -> List[Dict]:
        """Extract all questions from a PDF file."""
        questions = []
        filepath = os.path.join(self.pdf_dir, filename)
        
        if not os.path.exists(filepath):
            return questions
        
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    
                    # Split into individual questions
                    question_blocks = self._split_into_questions(text)
                    
                    for block in question_blocks:
                        questions.append({
                            'source': filename,
                            'page': page_num + 1,
                            'text': block,
                            'topics': self._identify_topics(block)
                        })
        except Exception as e:
            print(f"Error reading {filename}: {e}")
        
        return questions
    
    def _split_into_questions(self, text: str) -> List[str]:
        """Split page text into individual questions."""
        lines = text.split('\n')
        questions = []
        current_question = []
        
        for line in lines:
            # Check if line starts with a question number
            if re.match(r'^\s*\d+\.\s+', line.strip()):
                if current_question:
                    questions.append('\n'.join(current_question))
                current_question = [line]
            elif current_question:
                current_question.append(line)
        
        if current_question:
            questions.append('\n'.join(current_question))
        
        return questions
    
    def _identify_topics(self, question_text: str) -> List[str]:
        """Identify which topics/chapters a question relates to based on keywords."""
        topics = []
        text_lower = question_text.lower()
        
        for topic_num, keywords in TOPIC_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    topics.append(topic_num)
                    break
        
        return list(set(topics))  # Remove duplicates
    
    def get_questions_by_topics(self, selected_topics: List[str], max_questions: int = None) -> List[Dict]:
        """Get questions that match the selected topics."""
        all_questions = []
        
        print(f"Scanning test banks: {', '.join(self.test_banks)}...")
        
        for tb_file in self.test_banks:
            print(f"  Reading {tb_file}...")
            questions = self.extract_questions_from_pdf(tb_file)
            all_questions.extend(questions)
        
        print(f"Total questions extracted: {len(all_questions)}")
        
        # Filter questions that match any of the selected topics
        matching_questions = []
        for question in all_questions:
            if any(topic in question['topics'] for topic in selected_topics):
                matching_questions.append(question)
        
        print(f"Questions matching selected chapters: {len(matching_questions)}")
        
        # Limit to max_questions if specified
        if max_questions and max_questions > 0:
            matching_questions = matching_questions[:max_questions]
        
        return matching_questions


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 80)
    print("AP CALCULUS QUESTION SELECTOR")
    print("=" * 80)


def select_course():
    """Prompt user to select course."""
    print("\nSelect Course:")
    print("1. AP Calculus AB")
    print("2. AP Calculus BC")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == "1":
            return "AB"
        elif choice == "2":
            return "BC"
        else:
            print("Invalid choice. Please enter 1 or 2.")


def display_chapters(course: str):
    """Display available chapters for the course."""
    chapters = AP_CALCULUS_AB_CHAPTERS.copy()
    if course == "BC":
        chapters.update(AP_CALCULUS_BC_ADDITIONAL)
    
    print(f"\nAvailable Chapters for AP Calculus {course}:")
    print("-" * 80)
    for chapter_num in sorted(chapters.keys(), key=int):
        print(f"  {chapter_num}. {chapters[chapter_num]}")
    
    return chapters


def select_chapters(chapters: Dict[str, str]) -> List[str]:
    """Prompt user to select chapters."""
    print("\nSelect Chapters:")
    print("Enter chapter numbers separated by commas (e.g., 1,2,3)")
    print("Or enter a range (e.g., 1-4)")
    
    while True:
        selection = input("\nYour selection: ").strip()
        
        try:
            selected = []
            
            # Handle ranges and individual numbers
            parts = selection.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    selected.extend([str(i) for i in range(start, end + 1)])
                else:
                    # Individual number
                    selected.append(part)
            
            # Validate selections
            valid_selections = []
            for s in selected:
                if s in chapters:
                    valid_selections.append(s)
                else:
                    print(f"Warning: Chapter {s} is not valid and will be ignored.")
            
            if valid_selections:
                return valid_selections
            else:
                print("No valid chapters selected. Please try again.")
        
        except Exception as e:
            print(f"Invalid input format: {e}. Please try again.")


def get_question_count():
    """Prompt user for number of questions."""
    print("\nNumber of Questions:")
    
    while True:
        count = input("Enter the number of questions to retrieve (0 for all): ").strip()
        try:
            num = int(count)
            if num < 0:
                print("Please enter a non-negative number.")
            else:
                return num
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_results(questions: List[Dict]):
    """Display the search results."""
    print("\n" + "=" * 80)
    print("SEARCH RESULTS")
    print("=" * 80)
    
    if not questions:
        print("\nNo questions found matching the selected criteria.")
        return
    
    print(f"\nFound {len(questions)} matching questions:\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 80}")
        print(f"Question {i}:")
        print(f"Source: {question['source']}, Page {question['page']}")
        print(f"Topics: {', '.join(['Chapter ' + t for t in question['topics']])}")
        print("-" * 80)
        
        # Display question text (truncate if too long)
        text = question['text']
        if len(text) > 800:
            print(text[:800] + "...")
        else:
            print(text)
    
    print(f"\n{'=' * 80}\n")


def save_results(questions: List[Dict], filename: str = "selected_questions.txt"):
    """Save results to a file."""
    if not questions:
        print("No questions to save.")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("AP CALCULUS SELECTED QUESTIONS\n")
            f.write("=" * 80 + "\n\n")
            
            for i, question in enumerate(questions, 1):
                f.write(f"\nQuestion {i}:\n")
                f.write(f"Source: {question['source']}, Page {question['page']}\n")
                f.write(f"Topics: {', '.join(['Chapter ' + t for t in question['topics']])}\n")
                f.write("-" * 80 + "\n")
                f.write(question['text'])
                f.write("\n" + "=" * 80 + "\n")
        
        print(f"\nResults saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """Main entry point for the CLI application."""
    display_menu()
    
    # Select course
    course = select_course()
    
    # Display and select chapters
    chapters = display_chapters(course)
    selected_chapters = select_chapters(chapters)
    
    print(f"\nSelected chapters: {', '.join(selected_chapters)}")
    for ch in selected_chapters:
        print(f"  Chapter {ch}: {chapters[ch]}")
    
    # Get question count
    num_questions = get_question_count()
    
    # Search for questions
    print("\n" + "=" * 80)
    print("SEARCHING...")
    print("=" * 80)
    
    extractor = QuestionExtractor()
    max_q = num_questions if num_questions > 0 else None
    matching_questions = extractor.get_questions_by_topics(selected_chapters, max_q)
    
    # Display results
    display_results(matching_questions)
    
    # Offer to save results
    if matching_questions:
        save_choice = input("Would you like to save the results to a file? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter filename (default: selected_questions.txt): ").strip()
            if not filename:
                filename = "selected_questions.txt"
            save_results(matching_questions, filename)


if __name__ == "__main__":
    main()
