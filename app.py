from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = "inventory.csv"

<h1>FreshGuard CI/CD Test</h1>
# Create CSV if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Product", "ExpiryDate"])
        df.to_csv(CSV_FILE, index=False)


# Read inventory
def load_inventory():
    return pd.read_csv(CSV_FILE)


# Save inventory
def save_inventory(df):
    df.to_csv(CSV_FILE, index=False)


# Determine product status
def calculate_status(expiry_date):

    today = datetime.today().date()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    days_left = (expiry - today).days

    if days_left < 0:
        status = "Expired"
    elif days_left <= 7:
        status = "Expiring Soon"
    else:
        status = "Fresh"

    return status, days_left


@app.route("/")
def dashboard():

    df = load_inventory()

    products = []

    for _, row in df.iterrows():

        status, days_left = calculate_status(row["ExpiryDate"])

        products.append({
            "product": row["Product"],
            "expiry": row["ExpiryDate"],
            "days_left": days_left,
            "status": status
        })

    return render_template("dashboard.html", products=products)


@app.route("/add", methods=["POST"])
def add_product():

    product = request.form["product"]
    expiry = request.form["expiry"]

    df = load_inventory()

    new_row = pd.DataFrame([{
        "Product": product,
        "ExpiryDate": expiry
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    save_inventory(df)

    return redirect("/")


@app.route("/download")
def download_report():

    df = load_inventory()

    report = []

    for _, row in df.iterrows():

        status, days_left = calculate_status(row["ExpiryDate"])

        if status != "Fresh":

            report.append({
                "Product": row["Product"],
                "ExpiryDate": row["ExpiryDate"],
                "DaysLeft": days_left,
                "Status": status
            })

    report_df = pd.DataFrame(report)

    # report_file = "expired_report.csv"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_file = f"expired_report_{timestamp}.csv"

    report_df.to_csv(report_file, index=False)

    return send_file(
        report_file,
        as_attachment=True
    )


if __name__ == "__main__":

    initialize_csv()

    app.run(host="0.0.0.0", port=5000, debug=True)