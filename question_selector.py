#!/usr/bin/env python3
"""
AP Calculus Question Selector

This program allows users to select a subset of questions from AP Calculus test banks
matching specific College Board AP Calculus AB or BC chapters.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import PyPDF2
import os
import re
from typing import List, Dict, Tuple


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
                    
                    # Split into individual questions (questions typically start with a number followed by a period)
                    # This is a simplified approach
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
        # Simple approach: split by question numbers (1., 2., etc.)
        # This is a heuristic and may need refinement
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
        
        for tb_file in self.test_banks:
            questions = self.extract_questions_from_pdf(tb_file)
            all_questions.extend(questions)
        
        # Filter questions that match any of the selected topics
        matching_questions = []
        for question in all_questions:
            if any(topic in question['topics'] for topic in selected_topics):
                matching_questions.append(question)
        
        # Limit to max_questions if specified
        if max_questions and max_questions > 0:
            matching_questions = matching_questions[:max_questions]
        
        return matching_questions


class QuestionSelectorGUI:
    """GUI for selecting AP Calculus questions by chapter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AP Calculus Question Selector")
        self.root.geometry("900x700")
        
        self.extractor = QuestionExtractor()
        self.selected_chapters = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="AP Calculus Question Selector", 
                               font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Course selection
        course_label = ttk.Label(main_frame, text="Select Course:")
        course_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.course_var = tk.StringVar(value="AB")
        course_frame = ttk.Frame(main_frame)
        course_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(course_frame, text="AP Calculus AB", 
                       variable=self.course_var, value="AB",
                       command=self.update_chapter_list).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(course_frame, text="AP Calculus BC", 
                       variable=self.course_var, value="BC",
                       command=self.update_chapter_list).pack(side=tk.LEFT, padx=5)
        
        # Chapter selection label
        chapter_label = ttk.Label(main_frame, text="Select Chapters:")
        chapter_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Chapter listbox with scrollbar
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chapter_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, 
                                         height=10, yscrollcommand=scrollbar.set)
        self.chapter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chapter_listbox.yview)
        
        self.update_chapter_list()
        
        # Number of questions
        questions_label = ttk.Label(main_frame, text="Number of Questions (0 for all):")
        questions_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.num_questions_var = tk.StringVar(value="10")
        questions_entry = ttk.Entry(main_frame, textvariable=self.num_questions_var, width=10)
        questions_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Search button
        search_button = ttk.Button(main_frame, text="Search Questions", 
                                   command=self.search_questions)
        search_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Results label
        results_label = ttk.Label(main_frame, text="Results:")
        results_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(main_frame, height=20, width=100)
        self.results_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def update_chapter_list(self):
        """Update the chapter list based on selected course."""
        self.chapter_listbox.delete(0, tk.END)
        
        chapters = AP_CALCULUS_AB_CHAPTERS.copy()
        if self.course_var.get() == "BC":
            chapters.update(AP_CALCULUS_BC_ADDITIONAL)
        
        for chapter_num in sorted(chapters.keys(), key=int):
            chapter_name = chapters[chapter_num]
            self.chapter_listbox.insert(tk.END, f"Chapter {chapter_num}: {chapter_name}")
    
    def search_questions(self):
        """Search for questions matching selected criteria."""
        # Get selected chapters
        selected_indices = self.chapter_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one chapter.")
            return
        
        selected_topics = []
        for idx in selected_indices:
            chapter_text = self.chapter_listbox.get(idx)
            # Extract chapter number
            chapter_num = chapter_text.split(":")[0].replace("Chapter ", "").strip()
            selected_topics.append(chapter_num)
        
        # Get number of questions
        try:
            num_questions = int(self.num_questions_var.get())
            if num_questions < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of questions (0 or positive integer).")
            return
        
        # Search for questions
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Searching for questions in chapters: {', '.join(selected_topics)}...\n\n")
        self.root.update()
        
        max_q = num_questions if num_questions > 0 else None
        matching_questions = self.extractor.get_questions_by_topics(selected_topics, max_q)
        
        # Display results
        if not matching_questions:
            self.results_text.insert(tk.END, "No questions found matching the selected criteria.\n")
        else:
            self.results_text.insert(tk.END, f"Found {len(matching_questions)} matching questions:\n\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            for i, question in enumerate(matching_questions, 1):
                self.results_text.insert(tk.END, f"Question {i}:\n")
                self.results_text.insert(tk.END, f"Source: {question['source']}, Page {question['page']}\n")
                self.results_text.insert(tk.END, f"Topics: {', '.join(['Chapter ' + t for t in question['topics']])}\n\n")
                self.results_text.insert(tk.END, question['text'][:500])  # Show first 500 chars
                if len(question['text']) > 500:
                    self.results_text.insert(tk.END, "...\n")
                else:
                    self.results_text.insert(tk.END, "\n")
                self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = QuestionSelectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
