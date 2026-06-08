# Algoritme som bruker salt & pepper X
# Krypteringsfunksjon X

from flask import Flask, render_template, request, redirect, session
from decorators import login_required
from werkzeug.exceptions import HTTPException
from user import User, get_all, db, init_db
from config import DevelopmentConfig
from pprint import pprint
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.secret_key = "3hfdsajfhskruk"


db.init_app(app)


with app.app_context():
    init_db()
    users = get_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/log-out")
def log_out():
    session.clear()
    return redirect("/")


@app.route("/register")
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    fornavn = request.form.get("fornavn", "").strip()
    etternavn = request.form.get("etternavn", "").strip()

    # Validering: Hvis brukernavn / passord er tomt
    if not username or not password or not fornavn or not etternavn:
        return render_template("register.html",
                               error_msg="Alle felt må fylles ut.",
                               form=request.form)

    if username.lower() in users:
        return render_template("register.html",
                               error_msg="Brukernavn finnes allerede.",
                               form=request.form)

    user = User(username=username, password=password,
                fornavn=fornavn, etternavn=etternavn)

    user.save_to_db()
    users[user.username] = user
    session["user"] = {"username": user.username, "fornavn": user.fornavn, "etternavn": user.etternavn}
    session["logged_in"] = True
    pprint(users)
    return redirect("/")


@app.route("/min-profil")
@login_required
def min_profil():
    return render_template("min_profil.html")


@app.route("/log-in")
def get_login():
    return render_template("login.html")


@app.route("/log-in", methods=["POST"])
def post_login():
    username = request.form.get("username", "").lower()
    password = request.form.get("password", "")


    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return render_template("login.html",
                               error_msg="Feil brukernavn eller passord.",
                               form=request.form)

    session["user"] = {"username": user.username, "fornavn": user.fornavn, "etternavn": user.etternavn}
    session["logged_in"] = True
    return redirect("/")


@app.route("/comment/<post_id>", methods=["POST"])
@login_required
def comment(post_id):
    comment_text = request.form.get("comment", "").strip()

    if not comment_text:
        return redirect(f"/post/{post_id}")
    return redirect(f"/post/{post_id}")


@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    fornavn = request.form.get("fornavn", "").strip()
    etternavn = request.form.get("etternavn", "").strip()

    if not fornavn or not etternavn:
        return render_template("min_profil.html",
                               error_msg="Alle felt må fylles ut.")

    # Update user in database
    username = session.get("user", {}).get("username")
    if not username:
        return redirect("/log-in")

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect("/log-in")

    user.fornavn = fornavn
    user.etternavn = etternavn
    # Commit the changes
    db.session.commit()

    session["user"]["fornavn"] = fornavn
    session["user"]["etternavn"] = etternavn

    return redirect("/min-profil")


# Dev mode:
if __name__ == "__main__":
    app.run(debug=True)

