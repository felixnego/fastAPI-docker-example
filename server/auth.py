import time 
import jwt
import os
import hashlib
from db import db_connection
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer


JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']


class JWTBearer(HTTPBearer):
    """
    Validation of JWT tokens for the secure routes.
    """
    def __init__(self, auto_error=True):
        # no need to call super() with params in Py3
        super().__init__(auto_error=auto_error)
    

    async def __call__(self, request: Request):
        """
        Make the class callable. 
        Verifies the token in the correct scheme.
        Raises HTTPException.
        """
        credentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid scheme!")
            if not self.__verify_token__(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token!")
            return credentials.credentials
        
        raise HTTPException(status_code=403, detail="Invalid authorization code!")
    

    def __verify_token__(self, jwt_token):
        """
        Validates the JWT token with external function
        provided in this module. Used in the Callable
        protocol.
        """
        if decode_token(jwt_token):
            return True
        return False


def return_token(token):
    """
    Return the token as a dictionary.
    """
    return {
        'jwt_token': token 
    }


def sign_token(user_email):
    """
    Create the JWT token using the user_id
    and sign it. Expires after 5 mintues.
    """
    payload = {
        "user_email": user_email,
        "exp": time.time() + 300
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return return_token(token)


def decode_token(token):
    """
    Attempts decoding the token. Returns None if
    unsuccessful. Expiry is automatically verified
    in jwt.decode() per documentation.
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        return None


async def verify_exists_user(user_login):
    # TODO: belongs in a separe, DB module
    """
    Check to see whether a certain email-password
    combination exists in the database.
    """
    conn = db_connection()
    query = "SELECT email, password FROM users"

    conn.execute(query)
    users = list(conn)

    password = hashlib.sha256(user_login.password.encode()).hexdigest()

    for user_email, user_password in users:
        if user_email == user_login.email and user_password == password:
            return True

    return False
    
