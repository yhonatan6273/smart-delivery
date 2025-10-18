from src.schemas import users
import pytest
from jose import jwt
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set



# test function to create a new user
def test_post_user(client):
    #sending a post request to the /users endpoint with email and password in json format
    res = client.post(
        "/users/",
        json={"email": "1111@gmail.com", "password": "password1"}
    )
   
    #creating a new object of UserOutput schema to validate the response data
    #res is the response object from the post request
    #we convert json response to dictionary using .json()
    # ** unpacks the dictionary into keyword arguments
    new_user = users.UserOutput(**res.json())
    assert res.status_code == 201
    assert new_user.email == "1111@gmail.com"
    return new_user


@pytest.mark.parametrize("email,password,status_code", [("testuser@gmail.com","password123",400),
                                                           ("testuser@gmail.com",None,422),
                                                           (None,"password123",422)])
# test function to create a user with an email that already exists
def test_incorrect_post_user(client,test_user,email,password,status_code):
    #trying to create a user with an email that already exists
    res = client.post(
        "/users/",
        json={"email": email, "password": password}
    )
    assert res.status_code == status_code
    

def test_get_user(client,test_user):
    #sending a get request to the /users/{id} endpoint with the test user id
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    user = users.UserOutput(**res.json())
    assert user.id == test_user['id']
    assert user.email == test_user['email']

def test_incorrect_get_user(client):
    #trying to get a user that does not exist
    res = client.get("/users/9999")
    assert res.status_code == 404
    
# test function to create a new user
def test_login_user(client,test_user):
    #sending a post request to the /login endpoint with email and password in form data format
    res = client.post(
        "/login",
        data={"username": test_user['email'], "password": test_user['password']}
    )
    res_login = users.Token(**res.json())
    assert res.status_code == 200
    #decode the token to get the payload
    payload = jwt.decode(res_login.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    #get the user id from the payload
    id = payload.get("user_id")
    #check if the id from the payload is the same as the test user id
    assert id == test_user['id']
    assert res_login.token_type == "bearer" 

@pytest.mark.parametrize("email,password,status_code", [("wrongemail@gmail.com","password123",403),
                                                           ("testuser@gmail.com","wrongpassword",403),
                                                           ("wrongemail@gmail.com","wrongpassword",403),
                                                           (None,"password123",403),
                                                           ("testuser@gmail.com",None,403)])
def test_incorrect_login_user(client,test_user,email,password,status_code):
    #trying to login with an incorrect password
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )
    assert res.status_code == status_code
    

