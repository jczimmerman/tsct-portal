import pytest


def test_create_course(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/course/create')
    assert b'Create New Course' in response.data
    # filling the form and Submit it
    response = client.post('/course/create', data={
        'majors': 'BUSA',
        'new_course': 'MATH 122',
        'course_description': 'Enter description here',
        'credits': '3'})
    # if it work redirect to the Home
    assert '/home' in response.headers['Location']
    response = client.get('/home')
    assert b'MATH 122'in response.data


def test_edit(client, auth):
    # getting the form as a teacher
    auth.login()
    response = client.get('/course/3/edit')
    assert b'Edit Course' in response.data
    assert b'CSET 180' in response.data
    # update the form the form and Submit it

    response = client.post('course/3/edit', data={
        'new_course': 'CSET 180',
        'course_description': 'This damn software project'})
    # redirect to home
    assert 'course/3/view' in response.headers['Location']
    response = client.get('course/3/view')
    assert b'CSET 180'in response.data


<<<<<<< HEAD
<<<<<<< HEAD
def test_delete(client, auth):
    # login to the page
    auth.login()
    response = client.post('/3/delete')
    assert '/home' in response.headers['Location']
    #testing failed delete
    response = client.get('/6/delete')
    assert b'Method Not Allowed' in response.data
=======
# def test_delete(client, auth):
#     # login to the page
#     auth.login()
#     response = client.post('/3/delete')
#     assert '/home' in response.headers['Location']
>>>>>>> ed99882b6e5a8add9db424140edb7152cff1cf26

=======
def test_delete(client, auth):
    # login to the page
    auth.login()
    # click the delete button to remove
    response = client.post('/course/3/delete')
    assert '/home' in response.headers['Location']
<<<<<<< HEAD
>>>>>>> 6cd3795fbc0ec2bb1247aa2f2368f02ea5aa7c4f
=======
    # make sure the course was removed
    assert b'CSET 180' not in response.data

>>>>>>> dd174fc58c7ae061fe11dc47f07a0d4b14fd5a6e

def test_view(client, auth):
    # login to the page
    auth.login()
    # get the course by clicking the view button
    response = client.get('course/1/view')
    assert b'Course Information' in response.data
