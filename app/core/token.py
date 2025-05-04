# app/core/token.py

from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "형의_비밀키"
ALGORITHM = "HS256"
