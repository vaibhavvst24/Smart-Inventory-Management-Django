from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import csv
import os

app = Flask(__name__)
app.secret_key = "inventory_secret"

CSV_FILE = "inventory.csv"

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Transaction Type", "Product", "Quantity"])


# Dashboard
@app.route("/")
def dashboard():
    transactions = []
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        transactions = list(reader)

    return render_template("dashboard.html", transactions=transactions)


# Add Transaction
@app.route("/add", methods=["POST"])
def add_transaction():

    transaction_type = request.form["transaction_type"]
    product = request.form["product"]
    quantity = request.form["quantity"]

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([transaction_type, product, quantity])

    flash("Transaction added successfully!")

    return redirect(url_for("dashboard"))


# Export CSV
@app.route("/export")
def export_csv():
    return send_file(CSV_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
