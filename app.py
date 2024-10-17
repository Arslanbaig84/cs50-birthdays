import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# defining months
months_31 = [1, 3, 5, 7, 8, 10, 12]
months_30 = [4, 6, 9, 11]
months_28 = [2]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        birthday_month = request.form.get("month")
        birthday_day = request.form.get("day")
        if name and birthday_month and birthday_day and int(birthday_month) >= 1 and int(birthday_month) <= 12 and int(birthday_day) >= 1 and int(birthday_day) <= 31:
            if int(birthday_month) in months_31 and int(birthday_day) <= 31 or int(birthday_month) in months_30 and int(birthday_day) <= 30 or int(birthday_month) in months_28 and int(birthday_day) <= 29:
        # TODO: Add the user's entry into the database
                db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, birthday_month, birthday_day)
                return redirect("/")
        return redirect("/")
    else:
        # TODO: Display the entries in the database on index.html
        rows = db.execute("SELECT id, name, month, day FROM birthdays;")
        people = []
        for row in rows:
            id = row["id"]
            name = row["name"]
            birthday_month = row["month"]
            birthday_day = row ["day"]
            birthday = f"{birthday_month}/{birthday_day}"
            people.append({"id": id, "name":name, "birthday":birthday})
        return render_template("index.html", people = people)


@app.route("/delete", methods=["POST"])
def delete():
    del_id = request.form.get("id")
    if del_id:
        db.execute("DELETE FROM birthdays WHERE id = ?", del_id)
        db.execute("UPDATE birthdays SET id = id -1 WHERE id > ?", del_id)
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    edit_id = request.form.get("id")
    if edit_id:
        row = db.execute("SELECT * FROM birthdays WHERE id = ?", edit_id)
        print(row)
        if row:
            return render_template("edit.html", id=edit_id, person=row[0])
    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    id = request.form.get("id")
    name = request.form.get("name")
    birthday_month = request.form.get("month")
    birthday_day = request.form.get("day")
    print(id)
    print(name)
    print(birthday_month)
    print(birthday_day)

    if name and birthday_month and birthday_day and int(birthday_month) >= 1 and int(birthday_month) <= 12 and int(birthday_day) >= 1 and int(birthday_day) <= 31:
        if int(birthday_month) in months_31 and int(birthday_day) <= 31 or int(birthday_month) in months_30 and int(birthday_day) <= 30 or int(birthday_month) in months_28 and int(birthday_day) <= 29:
            db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, birthday_month, birthday_day, id)

    return redirect("/")
