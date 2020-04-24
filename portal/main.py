from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("main", __name__)

# route for index template
@bp.route('/')
def index():
    return render_template('layouts/index.html')

# route for showing the home for teachers
@bp.route("/home", methods=['GET'])
@teacher_required
@login_required
def home():
    # user_id = session['user_id']
    cur = db.get_db().cursor()
    cur.execute(
        """SELECT courses.course_id, courses.name, courses.major, users.name AS teacher_name FROM courses INNER JOIN users ON courses.teacherid = users.id""")
    courses = cur.fetchall()
    cur.close()

    return render_template("layouts/home.html", courses=courses)


@bp.route("/home/mycourses", methods=['GET'])
@teacher_required
@login_required
def my_courses():

    user_id = session.get('user_id')

    cur = db.get_db().cursor()
    cur.execute(
        """SELECT courses.course_id, courses.name, courses.major,
        users.name AS teacher_name FROM courses
        INNER JOIN users ON courses.teacherid = users.id
        WHERE users.id = %s """,
        (user_id,))

    courses = cur.fetchall()
    cur.close()

    return render_template("layouts/home.html", courses=courses)
