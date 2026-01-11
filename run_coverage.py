#!/usr/bin/env python3
"""
Simple script to run test coverage analysis.

Usage:
    python run_coverage.py              # Run coverage and show terminal report
    python run_coverage.py --html       # Generate HTML coverage report
    python run_coverage.py --missing    # Show missing lines in terminal
"""

import subprocess
import sys
from pathlib import Path


def run_coverage(html=False, missing=False):
    """Run pytest with coverage analysis."""
    
    # Base command - use uv run for dev environment
    # Exclude tests that require spacy model (component_counter)
    cmd = [
        "uv", "run", "pytest",
        "--ignore=tests/test_component_counter.py",
        "--cov=utils",
        "--cov=data",
        "--cov-config=pyproject.toml",
        "--cov-report=term"
    ]
    
    # Add missing lines to terminal report
    if missing:
        cmd[-1] = "--cov-report=term-missing"
    
    # Add HTML report
    if html:
        cmd.append("--cov-report=html")
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if html and result.returncode == 0:
            html_path = Path("htmlcov") / "index.html"
            print(f"\n✓ HTML coverage report generated at: {html_path}")
            print(f"  Open with: open {html_path}")
        
        return result.returncode
    
    except FileNotFoundError:
        print("Error: uv or pytest not found. Make sure uv is installed and dev dependencies are available.")
        return 1


if __name__ == "__main__":
    html = "--html" in sys.argv
    missing = "--missing" in sys.argv
    
    sys.exit(run_coverage(html=html, missing=missing))
