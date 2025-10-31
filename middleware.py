import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from fastapi import Security

bearer = HTTPBearer()
load_dotenv()

secret_key = os.getenv("secret_key")

def create_token(details:dict, expiry):
    expire = datetime.now() + timedelta(minutes=expiry)

    details.update({"exp": expire})
    

    encoded_jwt = jwt.encode(details, secret_key)

    return encoded_jwt


def verify_token(request: HTTPAuthorizationCredentials=Security(bearer)):


    ## verify the token
    token = request.credentials
    verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])

    ## to verify the expiry time too

    expiry_time = verified_token.get("exp")


    return{
        "email" : verified_token.get("email"),
        "userType" : verified_token.get("userType"),
        "userId" : verified_token.get("userId")
    }
