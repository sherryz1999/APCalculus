"""
Configuration for AP Calculus Question Selector

This module contains shared configuration used by both the GUI and CLI versions
of the question selector.
"""

import os

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


def get_available_test_banks(pdf_dir: str = ".") -> list:
    """
    Get list of available test bank PDF files.
    
    Note: TB_2.pdf is not included in the repository. The available test banks
    are TB_1.pdf, TB_3.pdf, TB_4.pdf, TB_5.pdf, TB_6.pdf, and TB_7.pdf.
    
    Args:
        pdf_dir: Directory containing the PDF files
        
    Returns:
        List of available test bank filenames
    """
    # Expected test bank files (TB_2.pdf is missing from the repository)
    expected_files = [f"TB_{i}.pdf" for i in [1, 3, 4, 5, 6, 7]]
    
    # Filter to only include files that actually exist
    available = []
    for filename in expected_files:
        filepath = os.path.join(pdf_dir, filename)
        if os.path.exists(filepath):
            available.append(filename)
    
    return available
