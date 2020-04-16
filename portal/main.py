from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, login_role

bp = Blueprint("portal", __name__)


@bp.route('/')
def index():
    return render_template('layouts/index.html')


@bp.route("/home", methods=['GET', 'POST'])
@login_role
@login_required
def home():

    user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute(
        """SELECT courses.course_id, courses.name, courses.major, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id""")
    courses = cur.fetchall()
    cur.close()
    print(courses)

    return render_template("layouts/home.html", courses=courses)


@bp.route("/student")
@login_required
def student():
    return render_template("layouts/student-home.html")
