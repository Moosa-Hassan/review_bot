from flask import Flask, render_template, request, redirect, jsonify
from chatbot import (
    load_instructor_reviews,search_reviews_by_professor, search_reviews_by_subject,
    summarize_reviews, add_Instructor_review, load_course_reviews , add_Course_review
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    query = None
    if request.method == "POST":
        query = request.form.get("query")
        instructor_data = load_instructor_reviews()
        course_data = load_course_reviews()
        prof_matches = search_reviews_by_professor(query, instructor_data)
        subj_matches = search_reviews_by_subject(query, course_data)

        if prof_matches:
            response = summarize_reviews(query, prof_matches, "Instructor")
        elif subj_matches:
            response = summarize_reviews(query, subj_matches, "Course")
        else:
            response = "❌ No reviews found for that professor or subject."

    return render_template("index.html", response=response, query=query)

@app.route("/add_instructor_review", methods=["POST"])
def add_instructor_review():
    data = load_instructor_reviews()
    professor = request.form["professor"]
    subject = request.form["subject"]
    review = request.form["review"]
    stars = int(request.form["stars"])

    msg = add_Instructor_review(professor, subject, review, stars, data)
    return redirect("/")

@app.route("/add_course_review", methods=["POST"])
def add_course_review():
    data = load_course_reviews()
    subject = request.form["subject"]
    review = request.form["review"]
    stars = int(request.form["stars"])

    msg = add_Course_review(subject, review, stars, data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
