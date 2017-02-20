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
#    submit = wtforms.SubmitField('Log in')

class judgment(FlaskForm):
    technique = wtforms.SelectField('technique', choices=[(str(i), i) for i in range(0, 11)])
    production = wtforms.SelectField('production', choices=[(str(i), i) for i in range(0,11)])
    teamwork = wtforms.SelectField('teamwork', choices=[(str(i), i) for i in range(0, 11)])
    artistry = wtforms.SelectField('artistry', choices=[(str(i), i) for i in range(0, 11)])
    musicality = wtforms.SelectField('musicality', choices=[(str(i), i) for i in range(0,11)])
    show = wtforms.SelectField('show', choices=[(str(i), i) for i in range(0, 11)])
    creativity = wtforms.SelectField('creativity', choices=[(str(i), i) for i in range(0, 11)])
    submit = wtforms.SubmitField('OK')

class admin(FlaskForm):
    field = wtforms.SelectField('field', choices=[(str(i), i) for i in range(0, 11)])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
csrf = CsrfProtect(app)
csrf.init_app(app)




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
        user_id = get_userWhereLog(form.login.data).get('user_id')
        return redirect(url_for("mainStr", id=user_id))

@app.route("/<id>", methods=["GET", "POST"])
def mainStr(id):
    user = get_user(id)
    form = admin()
    if request.method == "GET" and user.get('login'):
        if user.get('role'):
            return render_template('admin.html', form = form)
        return render_template("jProfile.html", user = user)
    elif request.method == "POST":
        return "POST", 200

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

@app.route("/judgment/<id>", methods=["GET", "POST"])
def jComand(id):
    comand = get_comandInfo(id)
    form = judgment()
    if request.method == "GET":
        return render_template("judgment.html", form = form, comand = comand)
    elif request.method == "POST":
        return "POST", 200


@app.route("/update", methods=["GET", "POST"])
def update():
    #comand = get_comandInfo()
    form = admin()      #Change
    if request.method == "GET":
        return render_template("update.html", form = form, comand = comand)
    elif request.method == "POST":
        return "POST", 200



def get_userWhereLog(log):
    with postgresql.open("pq://postgres:070698@localhost/LKS") as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user[0]:
        return user[0]
    return{}

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

def get_comandInfo(id):
    with postgresql.open("pq://postgres:070698@localhost/LKS") as db:
        sel = db.prepare("SELECT * FROM comands WHERE comand_id=$1 ")
        com = sel(id)
    if com[0]:
        return com[0]
    return {}

def get_user(id):
    with postgresql.open("pq://postgres:070698@localhost/LKS") as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE user_id=$1 ")
        com = sel(id)
    if com[0]:
        return com[0]
    return {}

if __name__ == "__main__":
    app.run(debug=True,host="192.168.0.102")

###########################################################################
