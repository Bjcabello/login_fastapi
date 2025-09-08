from fastapi import APIRouter
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.exceptions import HTTPException
from jose import jwt


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = { 
            "bryan": {
                "username": "bryan", "email": "bjcabello55@gmail.com", "password": "123"},
            "nathaly": {
                "username": "nathaly", "email": "nathalyc33@gmail.com", "password": "123"}
        }


def encode_token(playload: dict)-> str:
    token = jwt.encode(playload, "my_jwt_secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)])-> dict:
    data = jwt.encode(token, "my_jwt_secret", algorithm=["HS256"])
    user = users.get(data["username"])
    return user

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="El usuario o contrasena no es correcto")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token}

@router.get("/users/profile")
def profile(my_token: Annotated[str, Depends(decode_token)]):
    return my_token