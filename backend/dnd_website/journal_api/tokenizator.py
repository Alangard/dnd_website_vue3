import jwt
from datetime import datetime, timedelta


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_token(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=60)
    return {
        "access_token": create_access_token(
            data={"user_id": 1}, expires_delta=access_token_expires
        ),
        "token_type": "Token",
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, 'django-insecure-3+n@28ce9p$%*k^=z#5s0%j43vmn0wjvrb6uz2&^2saqvtfz@h', algorithm=ALGORITHM)
    return encoded_jwt


token = create_token(4)
print(token)
