from fastapi import FastAPI, Body, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from model import UserModel, UserLoginModel
from auth import sign_token, verify_exists_user, JWTBearer, decode_token
from datetime import datetime


tags_metadata = [
    {
        "name": "home",
        "description": "Root entrypoint for the API"
    },
    {
        "name": "authentication",
        "description": "The API uses JWT for authentication."
    },
    {
        "name": "run",
        "description": "Validates the JWT token and returns 'Hello World'."
    },
    {
        "name": "me",
        "description": "Validates the JWT token and returns the information encoded in it."
    }
]


app = FastAPI(
    title="FastAPI Example",
    description="Learning basic JWT authentication with FastAPI.",
    version=0.1,
    openapi_tags=tags_metadata
)


@app.get("/", tags=["home"])
async def root():

    return "Hello, Felix"


@app.post("/login", tags=["authentication"])
async def login(
    user_login: UserLoginModel = Body(
        ...,
        example={
            "email": "test@sample.com",
            "password": "supersecure"
        }
    )
):
    # no need to schedule as a task manually
    # per FastAPI docs
    if await verify_exists_user(user_login):
        return sign_token(user_login.email)

    return {
        "UNAUTHORIZED ERROR": "Invalid credentials!"
    }


@app.get("/run", dependencies=[Depends(JWTBearer())], tags=["run"])
async def run():
    return "Hello, World"


@app.get("/me", dependencies=[Depends(JWTBearer())], tags=["me"])
async def me(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
):
    """
    Presents info encoded in the JWT token. The token itself
    is verified by the JWTBearer class through dependency
    injection. Execution of this route's functions means
    the token has already been validated.
    """
    decoded_token = decode_token(credentials.credentials)

    exp = datetime.utcfromtimestamp(
        decoded_token.get("exp")
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    return f"""
    Welcome! Your email is {decoded_token.get("user_email")}!
    Your token will expire on {exp}.
    """
