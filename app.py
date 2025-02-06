from flask import Flask, render_template, request, redirect, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Path for storing contact data
CONTACTS_FILE = "contacts.json"

# Load contacts from JSON file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save contacts to JSON file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required!")
            return redirect("/contact")

        # Save contact form submission
        contacts = load_contacts()
        contacts.append({"name": name, "email": email, "message": message})
        save_contacts(contacts)

        flash("Thank you for contacting us!")
        return redirect("/")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
