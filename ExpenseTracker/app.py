from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

DATABASE = "expenses.db"


# ---------------- DATABASE ----------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        amount_text = request.form.get("amount", "").strip()
        date = request.form.get("date", "")

        # Basic validation
        if not name or not amount_text:
            return redirect("/")

        try:
            amount = float(amount_text)

            if amount <= 0:
                return redirect("/")

        except ValueError:
            return redirect("/")

        # Date formatting
        if date:
            try:
                formatted_date = datetime.strptime(
                    date, "%Y-%m-%d"
                ).strftime("%d-%m-%Y")

            except ValueError:
                formatted_date = datetime.now().strftime("%d-%m-%Y")

        else:
            formatted_date = datetime.now().strftime("%d-%m-%Y")

        # Save expense into SQLite database
        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO expenses (name, amount, date)
            VALUES (?, ?, ?)
            """,
            (name, amount, formatted_date)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    # Get all expenses
    conn = get_db_connection()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    conn.close()

    # Calculate statistics
    total = sum(expense["amount"] for expense in expenses)

    transaction_count = len(expenses)

    average = (
        total / transaction_count
        if transaction_count > 0
        else 0
    )

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        transaction_count=transaction_count,
        average=average
    )


# ---------------- DELETE ----------------

@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)