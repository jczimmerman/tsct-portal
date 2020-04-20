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





def test_course_creation(client, auth):
    #get the form
    auth.login()
    response = client.get('/create')
    assert b'Create New Course' in response.data
    #fill the form and submit it
    response = client.post('/create', data = {
    'majors': 'GEND',
    'new_course': 'something',
    'course_description': 'thingy'}
    )

    assert '/home' in response.headers['Location']
    response = client.get('/home')
    assert b'thingy' in response.data



def test_course_edit(client, auth):
    auth.login()
    response = client.get('/1/edit')
    response = client.post('/1/edit', data = {
    'name': 'Pizza', 'major': 'GEND', 'description': 'something', 'teacherid': '001'}
    )
    assert '/home' in response.headers['location']
    response = client.get('/home')
    assert b'Pizza' in response.data
