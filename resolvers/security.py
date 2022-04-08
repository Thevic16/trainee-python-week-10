import os
from datetime import timedelta

from fastapi import APIRouter


from graphql_app.schemas.tokens import TokenType
from security.security import authenticate_user, create_access_token
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()  # take environment variables from .env.


def login_for_access_token(username: str, password: str) -> TokenType:
    user = authenticate_user(username, password)
    if not user:
        raise Exception("Incorrect username or password")

    access_token_expires = timedelta(
        minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenType(access_token=access_token, token_type="bearer")
