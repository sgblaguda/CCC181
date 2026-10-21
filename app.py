"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask('Qeazy')

SERVICES = [
    {"id": 1, "name": "Transcript of Records"},
    {"id": 2, "name": "Certificate of Enrollment"},
    {"id": 3, "name": "Certificate of Grades"},
    {"id": 4, "name": "Good Moral Certificate"},
    {"id": 5, "name": "Enrollment / Load Revision"},
    {"id": 6, "name": "Diploma Claiming"},
]

# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.
TICKETS = [
    {
        "number": 1,
        "name": "Juana Batumbakal",
        "student_id": "2023-0123",
        "email": "ana@msuiit.edu.ph",
        "service_id": 1,
        "priority": False,
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Olivia Rodrigo",
        "student_id": "2022-4567",
        "email": "ben@msuiit.edu.ph",
        "service_id": 2,
        "priority": True,
        "status": "waiting",
    },
    {
        "number": 3,
        "name": "Conan Gray",
        "student_id": "2021-8910",
        "email": "carla@msuiit.edu.ph",
        "service_id": 6,
        "priority": False,
        "status": "called",
    },
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join", methods=["GET", "POST"])
def join():
    # GET: show the empty form. POST: the form was submitted.
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name})
        # Redirect after POST so refreshing the page doesn't join twice.
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
