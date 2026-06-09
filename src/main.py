from flask import Flask, render_template, request, redirect, session
from decorators import login_required
from werkzeug.exceptions import HTTPException
from auth import hash_password
from user import User, get_all, db, init_db
from config import DevelopmentConfig
from pprint import pprint
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.secret_key = "3hfdsajfhskruk"  # dette burde vær gjemt i .env


db.init_app(app)

9
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
    new_username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    fornavn = request.form.get("fornavn", "").strip()
    etternavn = request.form.get("etternavn", "").strip()

    if not new_username or not password or not fornavn or not etternavn:
        return render_template("min_profil.html",
                               error_msg="Alle felt må fylles ut.")

    username = session.get("user", {}).get("username")
    if not username:
        return redirect("/log-in")

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect("/log-in")

    if new_username != username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return render_template("min_profil.html",
                                   error_msg="Det nye brukernavnet er allerede i bruk.")

        db.session.delete(user)
        db.session.commit()

        user = User(username=new_username,
                    password=password,
                    fornavn=fornavn,
                    etternavn=etternavn)
        db.session.add(user)
        db.session.commit()

        users.pop(username, None)
        users[new_username] = user
    else:
        user.fornavn = fornavn
        user.etternavn = etternavn
        user.password = hash_password(password, user.username)
        db.session.commit()

    session["user"] = {"username": user.username,
                        "fornavn": user.fornavn,
                        "etternavn": user.etternavn}

    return redirect("/min-profil")


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    username = session.get("user", {}).get("username")
    if not username:
        return redirect("/log-in")

    user = User.query.filter_by(username=username).first()                #eksamen
    if user:
        db.session.delete(user)
        db.session.commit()

    users.pop(username, None)
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

