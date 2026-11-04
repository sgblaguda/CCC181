import os
import re
from datetime import timedelta, timezone
 
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
 
from models import Service, Ticket, User, db
 
load_dotenv()
 
app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"
 
db.init_app(app)
migrate = Migrate(app, db)

MINUTES_PER_STUDENT = 10

PH_TIME = timezone(timedelta(hours=8))

@app.template_filter("local")
def local_time(value):
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

@app.cli.command("seed")
def seed():
    starting = [("Late enrollment", 15), ("Change of subjects", 10),
                ("Crediting", 15), ("Record correction", 10)]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes))
    db.session.commit()
    print("Services are ready.")

@app.context_processor
def inject_my_ticket():
    ticket_id = session.get("ticket_id")
    t = db.session.get(Ticket, ticket_id) if ticket_id else None
    if t and t.status in ("waiting", "called"):
        return {"my_ticket": t}
    return {"my_ticket": None}

@app.route("/")
def index():
    return render_template("index.html")

def people_ahead(t):
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.id < t.id))
    return db.session.scalar(stmt)

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return render_template("ticket.html", ticket=t, service=t.service, ahead=ahead,
                           wait=ahead * t.service.avg_minutes)

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status in ("waiting", "called"):
        t.status = "left"
        db.session.commit()
    if session.get("ticket_id") == ticket_id:
        session.pop("ticket_id")
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return {"status": t.status, "ahead": ahead, "wait": ahead * t.service.avg_minutes}


def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    student_id = form.get("student_id", "").strip().upper()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    elif len(name) > 80:
        errors["name"] = "Name must be 80 characters or fewer."
    if not re.fullmatch(r"[0-9-]{4,20}", student_id):
        errors["student_id"] = "Enter your student ID (letters, numbers and dashes only)."
    if email and (len(email) > 120 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)):
        errors["email"] = "Enter a valid email address, or leave it blank."
    if service is None:
        errors["service_id"] = "Choose the type of concern."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    user = db.session.scalar(db.select(User).filter_by(student_id=student_id))
    if user is None:
        user = User(name=name, student_id=student_id, email=email or None)
    else:
        user.name = name
        if email:
            user.email = email
    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    session.permanent = True
    session["ticket_id"] = ticket.id
    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/find")
def find_form():
    return render_template("find.html", form={})


@app.post("/find")
def find():
    form = request.form
    number = form.get("number", type=int)
    student_id = form.get("student_id", "").strip().lower()
    t = next((t for t in TICKETS if t["number"] == number
              and t["student_id"].lower() == student_id), None)
    if t is None:
        flash("We couldn't find that ticket. Check the ticket number and student ID.", "danger")
        return render_template("find.html", form=form), 400
    session.permanent = True
    session["ticket_id"] = t["number"]
    return redirect(url_for("ticket", ticket_id=t["number"]))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.status != "called", Ticket.id))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    rows = db.session.execute(
        db.select(Ticket.service_id, func.count())
        .where(Ticket.status == "waiting").group_by(Ticket.service_id)).all()
    waiting = dict(rows)
    services = all_services()
    counts = {s.id: waiting.get(s.id, 0) for s in services}
    return render_template("staff.html", queue=queue, services=services,
                           counts=counts, selected=service_id)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    stmt = db.select(Ticket).where(Ticket.status == "waiting").order_by(Ticket.id).limit(1)
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    nxt = db.session.scalar(stmt)
    if nxt is None:
        flash("No one is waiting.", "warning")
    else:
        nxt.status = "called"
        nxt.called_at = func.now()
        db.session.commit()
        who = nxt.user.name if nxt.user else "a student"
        flash(f"Called ticket #{nxt.id} ({who}).", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard", service_id=request.form.get("service_id", type=int)))

@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    required = "waiting" if action == "call" else "called"
    if t.status != required:
        flash(f"Ticket #{ticket_id} is {t.status}, so it can't be marked {new_status}.", "warning")
    else:
        t.status = new_status
        if new_status == "called":
            t.called_at = func.now()
        db.session.commit()
        flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard", service_id=request.form.get("service_id", type=int)))


if __name__ == "__main__":
    app.run(debug=True)