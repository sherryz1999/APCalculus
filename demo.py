#!/usr/bin/env python3
"""
Demo Script for AP Calculus Question Selector

This script demonstrates the functionality of the question selector
with various example scenarios.
"""

from question_selector_cli import QuestionExtractor, AP_CALCULUS_AB_CHAPTERS, AP_CALCULUS_BC_ADDITIONAL
import time


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def demo_basic_search():
    """Demonstrate basic search functionality."""
    print_section("DEMO 1: Basic Search - Chapters 1-4")
    
    extractor = QuestionExtractor()
    selected_chapters = ['1', '2', '3', '4']
    
    print("\nSearching for questions covering:")
    for ch in selected_chapters:
        print(f"  • Chapter {ch}: {AP_CALCULUS_AB_CHAPTERS[ch]}")
    
    print("\nRequesting: 3 questions")
    print("\nSearching...")
    
    questions = extractor.get_questions_by_topics(selected_chapters, max_questions=3)
    
    print(f"\n✓ Found {len(questions)} matching questions!\n")
    
    for i, q in enumerate(questions, 1):
        print(f"Question {i}:")
        print(f"  Source: {q['source']}, Page {q['page']}")
        print(f"  Topics: Chapter {', '.join(q['topics'])}")
        print(f"  Preview: {q['text'][:150]}...")
        print()


def demo_single_chapter():
    """Demonstrate single chapter search."""
    print_section("DEMO 2: Single Chapter Search - Chapter 5")
    
    extractor = QuestionExtractor()
    selected_chapters = ['5']
    
    print("\nSearching for questions covering:")
    print(f"  • Chapter 5: {AP_CALCULUS_AB_CHAPTERS['5']}")
    
    print("\nRequesting: 2 questions")
    print("\nSearching...")
    
    questions = extractor.get_questions_by_topics(selected_chapters, max_questions=2)
    
    print(f"\n✓ Found {len(questions)} matching questions!\n")
    
    for i, q in enumerate(questions, 1):
        print(f"Question {i}:")
        print(f"  Source: {q['source']}, Page {q['page']}")
        print(f"  Topics: Chapter {', '.join(q['topics'])}")
        print(f"  Preview: {q['text'][:150]}...")
        print()


def demo_all_ab_chapters():
    """Demonstrate searching all AB chapters."""
    print_section("DEMO 3: All AP Calculus AB Chapters")
    
    extractor = QuestionExtractor()
    selected_chapters = list(AP_CALCULUS_AB_CHAPTERS.keys())
    
    print("\nSearching across ALL AP Calculus AB chapters:")
    for ch in selected_chapters:
        print(f"  • Chapter {ch}: {AP_CALCULUS_AB_CHAPTERS[ch]}")
    
    print("\nRequesting: 5 questions total")
    print("\nSearching...")
    
    questions = extractor.get_questions_by_topics(selected_chapters, max_questions=5)
    
    print(f"\n✓ Found {len(questions)} matching questions!\n")
    
    # Show distribution by chapter
    topic_counts = {}
    for q in questions:
        for topic in q['topics']:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    print("Topic distribution:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: int(x[0])):
        print(f"  Chapter {topic}: {count} question(s)")
    print()


def demo_bc_topics():
    """Demonstrate BC-specific topics."""
    print_section("DEMO 4: AP Calculus BC Specific Topics")
    
    extractor = QuestionExtractor()
    bc_chapters = list(AP_CALCULUS_BC_ADDITIONAL.keys())
    
    print("\nSearching for BC-specific topics:")
    for ch in bc_chapters:
        print(f"  • Chapter {ch}: {AP_CALCULUS_BC_ADDITIONAL[ch]}")
    
    print("\nRequesting: 2 questions")
    print("\nSearching...")
    
    questions = extractor.get_questions_by_topics(bc_chapters, max_questions=2)
    
    if questions:
        print(f"\n✓ Found {len(questions)} matching questions!\n")
        for i, q in enumerate(questions, 1):
            print(f"Question {i}:")
            print(f"  Source: {q['source']}, Page {q['page']}")
            print(f"  Topics: Chapter {', '.join(q['topics'])}")
            print(f"  Preview: {q['text'][:150]}...")
            print()
    else:
        print("\n⚠ No questions found for BC-specific topics.")
        print("This may indicate limited BC content in current test banks.")


def demo_statistics():
    """Show statistics about the test bank."""
    print_section("DEMO 5: Test Bank Statistics")
    
    extractor = QuestionExtractor()
    
    print("\nAnalyzing all test banks...")
    
    all_questions = []
    for tb_file in extractor.test_banks:
        questions = extractor.extract_questions_from_pdf(tb_file)
        all_questions.extend(questions)
        print(f"  {tb_file}: {len(questions)} questions")
    
    print(f"\nTotal questions: {len(all_questions)}")
    
    # Count questions per topic
    topic_counts = {}
    for q in all_questions:
        for topic in q['topics']:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    print("\nQuestions by chapter:")
    all_chapters = {**AP_CALCULUS_AB_CHAPTERS, **AP_CALCULUS_BC_ADDITIONAL}
    for chapter_num in sorted(all_chapters.keys(), key=int):
        count = topic_counts.get(chapter_num, 0)
        chapter_name = all_chapters[chapter_num]
        print(f"  Chapter {chapter_num} ({chapter_name}): {count} questions")
    
    # Questions with no topic identified
    no_topic = sum(1 for q in all_questions if not q['topics'])
    print(f"\nQuestions without identified topics: {no_topic}")


def main():
    """Run all demonstrations."""
    print_section("AP CALCULUS QUESTION SELECTOR - DEMONSTRATION")
    print("\nThis demo shows various ways to use the question selector.\n")
    input("Press Enter to continue...")
    
    # Run demos
    demo_basic_search()
    input("\nPress Enter for next demo...")
    
    demo_single_chapter()
    input("\nPress Enter for next demo...")
    
    demo_all_ab_chapters()
    input("\nPress Enter for next demo...")
    
    demo_bc_topics()
    input("\nPress Enter for next demo...")
    
    demo_statistics()
    
    print_section("DEMONSTRATION COMPLETE")
    print("\nTo use the interactive question selector, run:")
    print("  python3 question_selector_cli.py")
    print("\nFor GUI version (if Tkinter is available), run:")
    print("  python3 question_selector.py")
    print("\nFor more information, see USAGE.md")
    print()


if __name__ == "__main__":
    main()
