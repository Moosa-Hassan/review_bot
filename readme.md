# LLM-Based Review System for Courses and Instructors

## What It Does
Uses a Large Language Model (LLM) to analyze a large number of course or instructor reviews and produce a concise, structured summary.

## Purpose of the Project
Student reviews play an important role in deciding whether to take a course or study under a particular instructor. However, raw reviews can be biased, incomplete, or overwhelming in number.  
This project uses an LLM to condense multiple reviews into a short, fixed-size summary that highlights common patterns rather than individual opinions.

The output includes:
- Overall summary of reviews
- List of strengths
- List of weaknesses
- Advice for students

## How to Run
1. Navigate to the project root directory  
2. Run:
```bash
python api/app.py
```