from flask import Flask, render_template, g, redirect, url_for, Blueprint, request, session

from . import db
from portal.auth import login_required, teacher_required
from portal.session import get_session

bp = Blueprint("roster", __name__)

# Route to roster
@bp.route("/<int:id>/roster", methods=('GET', 'POST'))
def view(id):
    # session_id = class_session['id']
    bname = ''
    message=''
    con = db.get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT roster.student_id, roster.session_id, users.id, users.name
        FROM roster JOIN users ON roster.student_id = users.id
        WHERE session_id = %s ORDER BY users.name DESC""",
        (id,))
    students = cur.fetchall()
    cur.execute("""SELECT sessions.id, sessions.course_id, courses.course_id, courses.teacherid AS session_teacher
                FROM sessions JOIN courses on sessions.course_id = courses.course_id
                WHERE sessions.id = %s""",
                (id,))
    check = cur.fetchone()
    session_teacher = check['session_teacher']
    cur.close()
    if request.method == 'POST':
        studentname = request.form['sname']
        removename = request.form['rname']
        print(studentname)
        if studentname != "":
            cur = con.cursor()
            cur.execute('SELECT name, id FROM users WHERE name = %s',(studentname,))
            bname = cur.fetchone()
            print(bname)
            if bname is not None:
                bid = bname['id']
                cur.execute('SELECT student_id, session_id FROM roster WHERE student_id = %s AND session_id = %s',
                (bid, id))
                matching = cur.fetchall()
                if matching == []:
                    message = "{} added".format(studentname)
                    cur= con.cursor()
                    newid = bname['id']
                    print(newid)
                    cur.execute(
                    """INSERT INTO roster (student_id , session_id)
                    VALUES (%s, %s)""",
                    (newid,id))
                    con.commit()
                    cur.close()
                else:
                    message ="{} is already in the roster".format(studentname)
            else:
                message = "Error: student not found"
            cur.close()

        if removename != "":
            cur = con.cursor()
            cur.execute('SELECT name, id FROM users WHERE name = %s',(removename,))
            bname = cur.fetchone()
            print(bname)
            if bname is not None:
                bid = bname['id']
                cur.execute('SELECT student_id, session_id FROM roster WHERE student_id = %s AND session_id = %s',
                (bid, id))
                matching = cur.fetchall()
                print(matching)
                if matching != []:
                    message = "Student {} has been deleted".format(removename)
                    cur.execute('DELETE FROM roster WHERE session_id = %s AND student_id = %s',
                    (id,bid))
                    con.commit()
        if studentname == "" and removename == "":
            message = "error no input"
        con.close()
    return render_template("layouts/sessions/roster.html", students=students, session_teacher=session_teacher)
