from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session, abort

from . import db
from portal.auth import login_required, teacher_required

bp = Blueprint("session", __name__)


def get_session(id, check_teacher=True):

    user_id = session.get('user_id')
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.id, sessions.course_id, courses.teacherid
                FROM sessions LEFT JOIN courses on sessions.course_id = courses.course_id
                WHERE courses.teacherid = %s AND sessions.id = %s """,
                (user_id, id))
    x = cur.fetchone()
    cur.close()

    if x is None:
        abort(400, """System has prevented this action. \n
                    Either this session does not exist,\n
                    or you do not have acces to it.""")
    else:
        cur = db.get_db().cursor()
        cur.execute("""SELECT id, class_time, days, course_id, location
                    FROM sessions WHERE id = %s """,
                    (id,))
        class_session = cur.fetchone()
        cur.close()

        return class_session

# Route for viewing sessions
@bp.route("/<int:id>/sessions", methods=['GET', 'POST'])
@login_required
def view_sessions(id):
    """Single page view of session"""
    cur = db.get_db().cursor()
    cur.execute("""SELECT sessions.id, sessions.days, sessions.course_id,
                sessions.class_time, sessions.location, courses.name AS course_name,
                courses.teacherid AS teacher_id
                FROM sessions JOIN courses ON courses.course_id = sessions.course_id
                WHERE sessions.course_id = %s""",
                (id,))
    sessions = cur.fetchall()
    cur.close()

    return render_template("layouts/sessions/view_sessions.html", sessions=sessions)


@login_required
@teacher_required
@bp.route("/sessions/<int:id>/edit", methods=['GET', 'POST'])
def session_edit(id):
    """Edit a session"""
    session = get_session(id)
    if request.method == 'POST':

        session_days = request.form['session_days']
        session_time = request.form['session_time']
        location = request.form['location']

        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE sessions SET days = %s, class_time = %s, location = %s'
            ' WHERE id = %s ',
            (session_days, session_time, location, id)
        )
        g.db.commit()
        g.db.close()

        return redirect(url_for('session.view_sessions', id=session['course_id']))

    return render_template("layouts/sessions/edit_session.html", session=session)


@bp.route("/sessions/create", methods=['GET', 'POST'])
@login_required
@teacher_required
def create():

    user_id = session.get('user_id')
    cur = db.get_db().cursor()
    cur.execute("""
        SELECT course_id, name FROM courses where teacherid=%s""",
                (user_id,))
    courses = cur.fetchall()
    cur.close()

    if courses == None:
        abort(400, 'Either the course does not exist, or you do not have permission to create session for this course.')

    if request.method == 'POST':

        course = request.form['courses']
        cur = db.get_db().cursor()
        cur.execute("""
            SELECT course_id FROM courses where name=%s""",
                    (course,))
        x = cur.fetchone()
        cur.close()
        course_id = x['course_id']
        days = request.form['session_days']
        class_time = request.form['class_time']
        print(course, course_id, days, class_time)
        location = request.form['location']
        cur = db.get_db().cursor()
        cur.execute("""
        INSERT INTO sessions ( course_id, days, class_time, location)
        VALUES ( %s, %s, %s, %s)""",
                    (course_id, days, class_time, location))

        g.db.commit()
        cur.close()
        return redirect(url_for('session.view_sessions', id=course_id))

    return render_template("layouts/sessions/create_session.html", courses=courses)


@bp.route("/session/<int:id>/delete", methods=['POST', 'GET'])
@teacher_required
@login_required
def delete_session(id):
    """Delete unwanted session"""
    x = get_session(id)
    course_id = x['course_id']
    id = x['id']
    cur = db.get_db().cursor()
    cur.execute('DELETE FROM sessions where id = %s',
                (id,))
    g.db.commit()
    cur.close()

    return redirect(url_for('session.view_sessions', id=course_id))
    con.close()
    return redirect(url_for('session.view_sessions', course_id=course_id))


@bp.route("/home/my_sessions", methods=['GET'])
@teacher_required
@login_required
def my_sessions():

    user_id = session.get('user_id')
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""SELECT name FROM users where id = %s """,
                (user_id,))
    teacher_name = cur.fetchone()

    cur.execute("""SELECT courses.name as class_name, users.name as teacher_name,
            sessions.id as session_id, sessions.days as class_days, sessions.class_time as class_time,
            sessions.course_id as course_id, sessions.location as loca
            FROM users JOIN courses on users.id = courses.teacherid
            JOIN sessions on courses.course_id = sessions.course_id
            WHERE users.id =  %s ORDER BY sessions.course_id ASC """,
                (user_id,))
    sessions = cur.fetchall()
    cur.close()
    con.close()

    return render_template("layouts/sessions/my_sessions.html", sessions=sessions, teacher_name=teacher_name)


@bp.route("/home/my_sessions/<int:id>/delete", methods=['POST'])
@teacher_required
@login_required
def delete_my_session(id):
    """Delete unwanted session"""

    session = get_session(id)
    id = session['id']
    con = db.get_db()
    cur = con.cursor()
    cur.execute('DELETE FROM sessions where id = %s',
                (id,))
    g.db.commit()

    user_id = session.get('user_id')
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""SELECT name FROM users where id = %s """,
                (user_id,))
    teacher_name = cur.fetchone()

    cur.execute("""SELECT courses.name as class_name, users.name as teacher_name,
            sessions.id as session_id, sessions.days as class_days, sessions.class_time as class_time,
            sessions.course_id as course_id, sessions.location as loca
            FROM users JOIN courses on users.id = courses.teacherid
            JOIN sessions on courses.course_id = sessions.course_id
            WHERE users.id =  %s ORDER BY sessions.course_id ASC """,
                (user_id,))
    sessions = cur.fetchall()
    cur.close()
    con.close()

    return redirect(url_for("session.my_sessions", sessions=sessions, teacher_name=teacher_name))
