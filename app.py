from flask import Flask, render_template, request, session
import random
from books import books

app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # Required for session storage

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Recommend ALL matching books
@app.route("/recommend", methods=["POST"])
def recommend():
    mood = request.form["mood"]
    genre = request.form["genre"]

    # Filter matching books
    matched_books = [
        book for book in books
        if book["mood"] == mood and book["genre"] == genre
    ]

    # Save the matched list in session so Random can use it later
    session["matched_books"] = matched_books

    return render_template("results.html", books=matched_books)

# Random Book (from last recommended set)
@app.route("/random")
def random_book():
    matched_books = session.get("matched_books", [])

    if matched_books:
        # Pick one random book from the last recommended set
        book = random.choice(matched_books)
        return render_template("results.html", books=matched_books, random_book=book)
    else:
        # If no recommend was done yet, show one random from all books
        book = random.choice(books)
        return render_template("results.html", books=books, random_book=book)

# View All Books
@app.route("/all")
def all_books():
    return render_template("all_books.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)
