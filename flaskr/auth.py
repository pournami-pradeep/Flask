from flask import Blueprint, flash, redirect, render_template, request, url_for

from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()

        error = None
        if not username:
            error = "Please enter username"
        elif not password:
            error = "Please enter password"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html")
