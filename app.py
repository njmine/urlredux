from flask import Flask, render_template, request, redirect
from db import get_db, init_db
from utils import generate_short_code
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "change-this"

# initialize database tables if needed
with app.app_context():
    init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("url")

        if not original_url:
            return render_template("index.html", error="Please enter a URL.")

        # generate a unique short code
        short_code = generate_short_code()

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
            (short_code, original_url)
        )
        db.commit()

        return render_template("success.html", short_code=short_code)

    return render_template("index.html")


@app.route("/<short_code>")
def redirect_short(short_code):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = %s",
        (short_code,)
    )
    result = cursor.fetchone()

    if result:
        return redirect(result[0])
    else:
        return "Short URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
