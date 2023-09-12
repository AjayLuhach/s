import requests

def test_homepage():
    #send a request to home endpoint
    response = requests.post('http://localhost:80/')

    # check the response status  
    assert response.status_code == 200
     
 
 
 
def test_create_user():
    # Define the test data
    params = {
        'username': 'ajay88',
        'password1': 'password',   
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com'
    }
    

    
    response = requests.post('http://localhost/create', params=params)
 
    assert response.status_code == 200  #assume a successful response whichis status code of 200
    assert "created user" in response.text  #the response contains "created user"
    

 
def test_login_user():
    params = {
        'username': 'ajay88',
        'password': 'password',
    }
    response = requests.post('http://localhost/login', params=params)
    
    assert response.status_code == 200 #assume a successful response
    assert "login successful" in response.text #the response contains "login successful"
    params = {'username':'ajay88'}
    response = requests.delete('http://localhost/delete', params=params)