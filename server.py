from flask import Flask, render_template, request, redirect, url_for, session
import json
import postgresql
import random
from flask_wtf import FlaskForm
import wtforms
from flask_wtf.csrf import CsrfProtect
from werkzeug.utils import secure_filename
import os
import string
import hashlib
from wtforms.validators import Required, EqualTo

class Log_in(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Password", validators=[Required()])
    submit = wtforms.SubmitField('Log in')

class judgment(FlaskForm):
    technique = wtforms.SelectField('technique', choices=[(str(i), i) for i in range(1, 11)])
    production = wtforms.SelectField('production', choices=[(str(i), i) for i in range(1,11)])
    teamwork = wtforms.SelectField('teamwork', choices=[(str(i), i) for i in range(1, 11)])
    artistry = wtforms.SelectField('artistry', choices=[(str(i), i) for i in range(1, 11)])
    musicality = wtforms.SelectField('musicality', choices=[(str(i), i) for i in range(1,11)])
    show = wtforms.SelectField('show', choices=[(str(i), i) for i in range(1, 11)])
    creativity = wtforms.SelectField('creativity', choices=[(str(i), i) for i in range(1, 11)])
    submit = wtforms.SubmitField('OK')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'




@app.route("/home")
@app.route("/")
def home():
    return redirect(url_for("log_in"))

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    form = Log_in()
    if request.method == "GET":
        return render_template('log_in.html', form = form)
    elif request.method == "POST" :
        return redirect(url_for("mainStr", id="qwe"))

@app.route("/<id>")
def mainStr(id):
    form = judgment()
    return render_template("judgment.html", form = form)

@app.route("/api/log_in", methods=["GET", "POST"])
def log_in_api():
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        if data.get("action") == "ch_login_pass":
            if not check_logIs(data.get("login")):
                return "uncorrect_log", 200
            elif not check_passIs(data.get("login"), data.get("pass")):
                return "uncorrect_pass", 200
            return "Ok", 200

def check_logIs(log):
    with postgresql.open("pq://postgres:070698@localhost/LKS") as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user:
        return True
    return False
def check_passIs(log, password):
    with postgresql.open("pq://postgres:070698@localhost/LKS") as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1 AND password=$2;")
        user = sel(log.lower(),hashlib.md5(password.encode('utf8')).hexdigest())
    if user:
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)

###########################################################################
