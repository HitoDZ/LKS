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
import Config

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
    field = wtforms.StringField('field', validators=[Required()])

class comands(FlaskForm):
    name = wtforms.StringField("name", validators=[Required()])
    nomination = wtforms.StringField("nomination", validators=[Required()])
    C_order = wtforms.StringField("C_order", validators=[Required()])

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
    if session.get('id'):
        return redirect(url_for('mainStr', id=session['id']))
    if request.method == "GET":
        return render_template('log_in.html', form = form)
    elif request.method == "POST" :
        user = get_userWhereLog(form.login.data)
        session['id'] = user.get('user_id')
        session['name'] = user.get('name')
        session['role'] = user.get('role')
        session['orderComand'] = 1
        return redirect(url_for("mainStr", id=session['id']))

@app.route("/<id>", methods=["GET", "POST"])
def mainStr(id):
    form = admin()
    comands = get_allComands(id)
    if request.method == "GET" and session.get('id') == id:
        if session.get('role'):
            return render_template('admin.html', form = form)
        return render_template("jProfile.html", user = session, comands = comands)
    elif request.method == "POST" and session.get('id') == id:
        return "POST", 200
    return redirect(url_for('log_in'))

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

@app.route("/judgment", methods=["GET", "POST"])
def jComand():
    comand = get_comandInfo(session['orderComand'])
    if not comand:
        return redirect(url_for('mainStr', id = session.get('id')))
    form = judgment()
    if request.method == "GET" and session.get('id') :
        return render_template("judgment.html", form = form, comand = comand)
    elif request.method == "POST":
        session['orderComand'] +=1
        insert_judgRes(session['id'], comand['comand_id'], form)
        return redirect(url_for('jComand'))


@app.route("/update/", methods=["GET", "POST"])
def update():
    #comand = get_comandInfo()
    form = admin()      #Change
    if request.method == "GET":
        return render_template("update.html", form = form)#, comand = comand)
    elif request.method == "POST":
        return "POST", 200

def insert_judgRes(iduser, idcom, form):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("INSERT INTO judge VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)")
        try:
            com = sel(int(random.random()*1000), iduser, idcom, int(form.technique.data),
            int(form.production.data), int(form.teamwork.data), int(form.artistry.data),
            int(form.musicality.data), int(form.show.data), int(form.creativity.data),
            int(form.technique.data)+int(form.production.data)+int(form.teamwork.data)+int(form.artistry.data)+
            int(form.musicality.data)+int(form.show.data)+int(form.creativity.data), 0)
        except Exception:
            print('No')

def get_allComands(id):                                   #Вот она
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM judge WHERE user_id=$1 ")
        jud = sel(id)
    return jud

def get_userWhereLog(log):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user:
        return user[0]
    return{}

def update_comand_order(name, order):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("UPDATE comands WHERE name=$1 SET c_order=$2;")
        user = sel(name, order)

def insert_command(id, name, nomination, order):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("INSERT INTO comands (comand_id, name, nomination, c_order) VALUES($1, $2, $3, $4)")
        user = sel(id, name, nomination, order)

def check_logIs(log):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user:
        return True
    return False

def check_passIs(log, password):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1 AND password=$2;")
        user = sel(log.lower(),hashlib.md5(password.encode('utf8')).hexdigest())
    if user:
        return True
    return False

def get_comandInfo(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM comands WHERE C_order=$1 ")
        com = sel(id)
    if com:
        return com[0]
    return {}

def get_user(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE user_id=$1 ")
        com = sel(id)
    if com:
        return com[0]
    return {}

if __name__ == "__main__":
    app.run(debug=True)# ,host="192.168.1.10")

###########################################################################
