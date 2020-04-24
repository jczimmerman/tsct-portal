import pytest

def test_student_view(client, auth):
    #The four seperate views for the
    auth.student_login()
    response = client.get('/student')
    assert b'Student Homepage' and b'METAL 255' in response.data
    #course view
    response = client.get('/course/6/view')
    assert b'Course Information' and b'Test Teacher 2' in response.data
    #Session view
    response = client.get('/course/6/sessions')
    assert b'Current Sessions for METAL 255' in response.data
    #assignment view
    response = client.get('course/6/session/8/assignments')
    assert b'Crazy Experiment Details' in response.data
