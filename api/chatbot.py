import json

INSTRUCTOR_FILE = "./reviews.json"
COURSE_FILE = "./course.json"

def load_instructor_reviews():
    """Load reviews from the JSON file."""
    with open(INSTRUCTOR_FILE, "r") as data:
        return json.load(data)
    
def load_course_reviews():
    """Load reviews from the JSON file."""
    with open(COURSE_FILE, "r") as data:
        return json.load(data)

def save_instructor_reviews(data):
    """Save updated reviews back to the JSON file."""
    with open(INSTRUCTOR_FILE, "w") as f:
        json.dump(data, f, indent=2)
        
def save_course_reviews(data):
    """Save updated reviews back to the JSON file."""
    with open(COURSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def search_reviews_by_professor(name, data):
    """Return all reviews that match a professor's name."""
    return [r for r in data["reviews"] if name.lower() in r.get("professor","").lower()]

def search_reviews_by_subject(subject, data):
    """Return all reviews that match a subject name."""
    return [r for r in data["reviews"] if subject.lower() in r.get("subject","").lower()]

def add_Instructor_review(professor, subject, review_text, stars, data):
    """Add a new review and save to file."""
    new_entry = {
        "professor": professor,
        "subject": subject,
        "review": review_text,
        "stars": stars
    }
    data["reviews"].append(new_entry)
    save_instructor_reviews(data)
    return "✅ Review added successfully!"

def add_Course_review(subject, review, stars, data):
    """Add a new review and save to file."""
    new_entry = {
        "subject": subject,
        "review": review,
        "stars": stars
    }
    data["reviews"].append(new_entry)
    save_course_reviews(data)
    return "✅ Review added successfully!"

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("review_bot_key"),
    base_url="https://openrouter.ai/api/v1"
)

def summarize_reviews(entity_name, reviews,who):
    if not reviews:
        return f"No reviews found for {entity_name}."

    if who=="Instructor":
        review_text = "\n".join([
            f"- {r['professor']} ({r['subject']}, {r['stars']}★): {r['review']}"
            for r in reviews
        ])
    elif who =="Course":
        review_text = "\n".join([
            f"- {r['subject']}, ({r['stars']}★): {r['review']}"
            for r in reviews
        ])
    #"\n".join([r["review"] for r in reviews])
    prompt =  f"""
    You are a helpful assistant that summarizes student reviews for professors.

    Here are actual reviews for "{entity_name}":

    {review_text}

    Use only this information — do not invent. If no weaknesses are mentioned, say "No significant weaknesses noted."

    Now summarize with this structure:

    If summarizing a professor, set:
    Instructor: {entity_name}

    If summarizing a course, set:
    Subject: {entity_name}


    Summary:
    <Short paragraph summarizing overall sentiment, teaching style, and trends in reviews.>

    Strengths:
    - ...

    Weaknesses:
    - ...

    Advice for Students:
    - ...
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
