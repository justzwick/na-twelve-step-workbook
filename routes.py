
from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, login_required
from .models import User, Step, Question, Answer
from .database import db

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("login.html")


@routes.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return redirect("/dashboard")

    return "Invalid login"


@routes.route("/dashboard")
@login_required
def dashboard():
    steps = Step.query.all()
    return render_template("dashboard.html", steps=steps)


@routes.route("/step/<int:step_id>")
@login_required
def step(step_id):
    questions = Question.query.filter_by(section_id=step_id).all()
    return render_template("step.html", questions=questions)


@routes.route("/question/<int:question_id>", methods=["GET", "POST"])
@login_required
def question(question_id):

    if request.method == "POST":
        answer_text = request.form["answer"]

        answer = Answer(
            question_id=question_id,
            answer_text=answer_text
        )

        db.session.add(answer)
        db.session.commit()

    question = Question.query.get(question_id)

    return render_template("question.html", question=question)
