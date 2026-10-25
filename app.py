"""Qeazy

Run it with:
    flask --app app run --debug
"""
import re
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me" 

SERVICES = [
    {"id": 1, "name": "Late enrollment"},
    {"id": 2, "name": "Change of subjects"},
    {"id": 3, "name": "Crediting"},
    {"id": 4, "name": "Record correction"},
]

# Each ticket: number, name, student_id, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Loi", "student_id": "2023-0123", "service_id": 2, "status": "called"},
    {"number": 2, "name": "Ben", "student_id": "2022-4567", "service_id": 1, "status": "waiting"},
    {"number": 3, "name": "Ana", "student_id": "2021-8910", "service_id": 3, "status": "waiting"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})

@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    student_id = form.get("student_id", "").strip()
    service_id = form.get("service_id", type=int)
 
    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    elif len(name) > 60:
        errors["name"] = "Name must be 60 characters or fewer."
    if not re.fullmatch(r"[A-Za-z0-9-]{4,20}", student_id):
        errors["student_id"] = "Enter your student ID (letters, numbers and dashes only)."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose the type of concern."
 
    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400
 
    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "student_id": student_id,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


if __name__ == "__main__":
    app.run(debug=True)