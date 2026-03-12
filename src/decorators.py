from flask import session, send_file, render_template, request
from functools import wraps

def login_required(fn):
    @wraps(fn)
    def _login_required(*args, **kwargs):
        if not session.get('logged_in'):
            return render_template("login.html", redirect_to=request.url)

        return fn(*args, **kwargs)
    return _login_required


