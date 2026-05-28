from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Create JWT Token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# Verify JWT Token
def verify_token(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    

    from fastapi import Depends, HTTPException

def get_current_user(user_data=Depends(verify_token)):
    return user_data


def require_role(role: str):
    def role_checker(user=Depends(verify_token)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Access Denied")
        return user
    return role_checker