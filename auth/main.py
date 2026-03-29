"""
JWT AUTHENTICATION MAIN FILE

Purpose:
---------
This file handles user registration, login, JWT token creation,
token validation, and protected routes.

What this file does:
--------------------
1. Registers new users with hashed passwords
2. Authenticates users during login
3. Generates JWT access tokens
4. Validates JWT tokens for protected routes
5. Allows access to routes only if token is valid

Endpoints:
----------
- POST /signup     -> create a new user
- POST /login      -> login and get access token
- GET /protected   -> access only with valid bearer token

Flow:
-----
Signup:
request body -> validate -> hash password -> save user

Login:
form data -> verify username/password -> generate token

Protected route:
bearer token -> decode token -> extract username -> allow access
"""


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "eptO1vffnR3PhXtCl4lZ6Wd45RhI1ybe0srguQAwwjA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# Helper function that takes user data

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.Usercreate, db: Session = Depends(get_db)):
    # check the user exists or not
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail = "Username already exists")

    # Hash the password
    hashed_pass = utils.hash_password(user.password)

    # Create new user instance
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the value (excluding password)
    return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Password")
    
    token_data = {'sub': user.username}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
           raise credential_exception
    
    except JWTError:
        raise credential_exception
    
    return {"username": username}


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user['username']} | You accessed a protected route"
    }
