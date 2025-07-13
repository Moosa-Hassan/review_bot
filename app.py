from flask import Flask, render_template, request, redirect, jsonify
from chatbot import (
    load_reviews,search_reviews_by_professor, search_reviews_by_subject,
    summarize_reviews, add_review
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    query = None
    if request.method == "POST":
        query = request.form.get("query")
        data = load_reviews()
        prof_matches = search_reviews_by_professor(query, data)
        subj_matches = search_reviews_by_subject(query, data)

        if prof_matches:
            response = summarize_reviews(query, prof_matches)
        elif subj_matches:
            response = summarize_reviews(query, subj_matches)
        else:
            response = "❌ No reviews found for that professor or subject."

    return render_template("index.html", response=response, query=query)

@app.route("/add", methods=["POST"])
def add():
    data = load_reviews()
    professor = request.form["professor"]
    subject = request.form["subject"]
    review = request.form["review"]
    stars = int(request.form["stars"])

    msg = add_review(professor, subject, review, stars, data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
