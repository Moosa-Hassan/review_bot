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

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("review_bot_key"),
    base_url="https://openrouter.ai/api/v1"
)

def summarize_reviews(entity_name, reviews):
    if not reviews:
        return f"No reviews found for {entity_name}."

    review_text = "\n".join([
        f"- {r['professor']} ({r['subject']}, {r['stars']}★): {r['review']}"
        for r in reviews
    ])
    #"\n".join([r["review"] for r in reviews])
    prompt = f"""
    You are a helpful assistant that summarizes teacher reviews for students.

    Based on the following reviews for "{entity_name}", provide:
    - A concise summary of overall sentiment
    - The teacher’s strengths and weaknesses
    - Practical advice for students taking their course
    
    

    Follow this **exact output format**:
   Subject: <Subject> (Professor Name)

    Instructor: <Full Professor Name>

    Summary:
    <One short paragraph summarizing sentiment, teaching style, and common student feedback.>

    Strengths:
    - <Point 1>
    - <Point 2>
    - ...

    Weaknesses:
    - <Point 1>
    - ...

    Advice for Students:
    - <Tip 1>
    - <Tip 2>
    - ...

    Strictly follow this formatting and avoid extra headers or markdown.
    """
    
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You summarize academic reviews."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7,
        max_tokens = 400,
    )

    return response.choices[0].message.content
