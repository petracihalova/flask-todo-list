from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from form import TaskForm, LoginForm, RegistrationForm
from models import db, Task, User

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Nastavení databáze
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"  # Cesta k databázi
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Nastavení pro přihlašování
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = TaskForm()
    tasks = Task.query.filter_by(completed=False, user_id=current_user.id).all()

    if form.validate_on_submit():
        # Uložení úkolu do databáze, pokud je validace úspěšná
        new_task = Task(
            title=form.title.data,
            details=form.details.data,
            priority=form.priority.data,
            user_id=current_user.id,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html", seznam_ukolu=tasks, formular=form)


@app.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete and task_to_delete.user_id == current_user.id:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task_to_edit = Task.query.get(task_id)
    if task_to_edit and task_to_edit.user_id == current_user.id:
        form = TaskForm(obj=task_to_edit)
        if form.validate_on_submit():
            task_to_edit.title = form.title.data
            task_to_edit.details = form.details.data
            task_to_edit.priority = form.priority.data
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("edit.html", form=form, task=task_to_edit)
    return redirect(url_for("index"))



@app.route("/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/completed")
@login_required
def show_completed():
    tasks = Task.query.filter_by(completed=True, user_id=current_user.id).all()
    return render_template("completed.html", seznam_ukolu=tasks)


@app.route("/uncomplete/<int:task_id>")
@login_required
def uncomplete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = False
    db.session.commit()
    return redirect(url_for("show_completed"))


@app.route("/table")
@login_required
def show_table():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("table.html", seznam_ukolu=tasks)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Uživatel existuje. Prosím vyberte si jiné uživatelské jméno.", "danger")
            return redirect(url_for("register"))

        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrace proběhla úspěšně. Prosím přihlaste se.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Přihlašovací údaje jsou nesprávné.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
