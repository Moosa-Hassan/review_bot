import json

DATA_FILE = "reviews.json"

def load_reviews():
    """Load reviews from the JSON file."""
    with open(DATA_FILE, "r") as data:
        return json.load(data)

def save_reviews(data):
    """Save updated reviews back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def search_reviews_by_professor(name, data):
    """Return all reviews that match a professor's name."""
    return [r for r in data["reviews"] if name.lower() in r["professor"].lower()]

def search_reviews_by_subject(subject, data):
    """Return all reviews that match a subject name."""
    return [r for r in data["reviews"] if subject.lower() in r["subject"].lower()]

def add_review(professor, subject, review_text, stars, data):
    """Add a new review and save to file."""
    new_entry = {
        "professor": professor,
        "subject": subject,
        "review": review_text,
        "stars": stars
    }
    data["reviews"].append(new_entry)
    save_reviews(data)
    return "✅ Review added successfully!"

import ollama

def summarize_reviews(entity_name, reviews):
    if not reviews:
        return f"No reviews found for {entity_name}."

    review_text = "\n".join([
        f"- {r['professor']} ({r['subject']}, {r['stars']}★): {r['review']}"
        for r in reviews
    ])

    prompt = f"""
    You are a helpful assistant that summarizes teacher reviews for students.

    Based on the following reviews for "{entity_name}", provide:
    - A concise summary of overall sentiment
    - The teacher’s strengths and weaknesses
    - Practical advice for students taking their course
    
    Ignore reviews that appear overly emotional, excessively biased, 
    or intended to harm rather than provide constructive feedback

    Reviews:
    {review_text}
    Respond using this exact format:

    Subject: <subject>
    Instructor: <professor name>

    Summary:
    <Brief paragraph summarizing tone, teaching style, and general feedback>

    Strengths:
    - <Point 1>
    - <Point 2>
    - ...

    Weaknesses:
    - <Point 1>
    - ...

    Advice for Students:
    - <Point 1>
    - ...
    """

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You summarize academic reviews."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']
