from portal import create_app
import pytest

def test_config(monkeypatch):
    # Default config
    assert not create_app().testing

    # Test config
    assert create_app({'TESTING': True}).testing

    # Prod config
    monkeypatch.setenv('DATABASE_URL', "pretend this is on heroku...")
    assert "heroku" in create_app().config['DB_URL']
    assert "require" in create_app().config['DB_SSLMODE']


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form method="post">' in response.data
    assert b'<label for="email">' in response.data
    assert b'<label for="password">' in response.data
    assert b'<input type="password" name="password" />' in response.data
    assert b'<input type="submit" value="Login" />' in response.data

def test_login(client, username, password):
    response = client.post('/', data={'email': 'duck@stevenscollege.edu', 'password': ''})
    assert 'http://localhost' == response.headers['Location']





# def test_teacher_email(client):
#     assert client.get('/').status_code == 200
#     response = client.post(
#         '/', data={'email': 'duck@stevenscollege.edu', 'password': """
#         hashed = auth.hash_pass(password[1].tobytes())
#
#         cur.execute(
#             'UPDATE users SET password = %s WHERE id = %s',
#             (hashed, looney))
#
#         con.commit("""}
#     )
#     assert 'http://localhost/home' == response.headers['Location']


def test_email_error(client):
    assert client.get('/').status_code == 200
    error = None
    response = client.post(
        '/', data={'email': 'duck@stevenscollege.edu', 'password': ''}
    )
    if 'http://localhost/' == response.headers['Location']:
        error = 'Incorrect email or password!'
    assert error == 'Incorrect email or password!'
#
#
# def test_course_creation(client):
#     assert client.get('/create').status_code == 200
#     response = client.post(
#         '/create', data={'name': 'Pizza', 'description': ''}
#     )
#     assert 'http://localhost/home' == response.headers['Location']
#     cur = db.get_db().cursor()
#     new_course_name = cur.execute('SELECT * FROM courses WHERE name = Pizza').fetchone()
#     assert new_course_name['name'] == 'Pizza'
