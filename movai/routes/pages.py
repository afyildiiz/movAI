import os

from flask import Blueprint, render_template, request
from flask_mail import Message

from movai.extensions import mail

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def welcome():
    return render_template("welcome.html")


@pages_bp.route("/home")
def home():
    return render_template("home.html")


@pages_bp.route("/card")
def card():
    return render_template("card.html")


@pages_bp.route("/contact")
def contact():
    return render_template("contact.html")


@pages_bp.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        comment = request.form["message"]

        msg = Message(
            "Yeni İletişim Formu Gönderimi",
            sender=email,
            recipients=[os.environ.get("MAIL_USERNAME")],
        )
        msg.body = f"İsim: {name}\nE-posta: {email}\n\n {comment}"
        mail.send(msg)

        return render_template("about.html", data="Message has been sent!")

    return render_template("about.html")
