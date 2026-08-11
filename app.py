import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from models import Contact
from repository import ContactRepository

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

repo = ContactRepository()

@app.route("/")
def index():
    contacts = repo.find_all()
    return render_template("index.html", contacts=contacts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        contact = Contact(
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone") or None,
            company=request.form.get("company") or None,
        )
        errors = contact.validate()
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("form.html", contact=contact, action="Create")
        repo.create(contact)
        flash("Contact created successfully", "success")
        return redirect(url_for("index"))
    return render_template("form.html", contact=Contact(), action="Create")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    contact = repo.find_by_id(id)
    if not contact:
        flash("Contact not found", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        contact.name = request.form.get("name", "").strip()
        contact.email = request.form.get("email", "").strip()
        contact.phone = request.form.get("phone") or None
        contact.company = request.form.get("company") or None
        errors = contact.validate()
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("form.html", contact=contact, action="Edit")
        repo.update(contact)
        flash("Contact updated successfully", "success")
        return redirect(url_for("index"))
    return render_template("form.html", contact=contact, action="Edit")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if repo.delete(id):
        flash("Contact deleted", "success")
    else:
        flash("Contact not found", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)