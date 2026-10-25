import re

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

MINUTES_PER_STUDENT = 10

SERVICES = [
    {"id": 1, "name": "Late enrollment"},
    {"id": 2, "name": "Change of subjects"},
    {"id": 3, "name": "Crediting"},
    {"id": 4, "name": "Record correction"},
]

TICKETS = [
    {"number": 1, "name": "Loi", "student_id": "2023-0123", "service_id": 2, "status": "called"},
    {"number": 2, "name": "Ben", "student_id": "2022-4567", "service_id": 1, "status": "waiting"},
    {"number": 3, "name": "Ana", "student_id": "2021-8910", "service_id": 3, "status": "waiting"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead),
                           wait=len(ahead) * MINUTES_PER_STUDENT)


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


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


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    queue.sort(key=lambda t: (t["status"] != "called", t["number"]))
    names = {s["id"]: s["name"] for s in SERVICES}
    counts = {s["id"]: sum(1 for t in TICKETS
                           if t["service_id"] == s["id"] and t["status"] == "waiting")
              for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES, names=names,
                           counts=counts, selected=service_id)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    nxt = next((t for t in TICKETS if t["status"] == "waiting"
                and (not service_id or t["service_id"] == service_id)), None)
    if nxt is None:
        flash("No one is waiting.", "warning")
    else:
        nxt["status"] = "called"
        flash(f"Called ticket #{nxt['number']} ({nxt['name']}).", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)
    required = "waiting" if action == "call" else "called"
    if t["status"] != required:
        flash(f"Ticket #{ticket_id} is {t['status']}, so it can't be marked {new_status}.", "warning")
    else:
        t["status"] = new_status
        flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard", service_id=request.form.get("service_id", type=int)))


if __name__ == "__main__":
    app.run(debug=True)