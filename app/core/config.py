DATABASE_URL = "mysql+pymysql://root:1219@localhost:3306/jmemo"

import os

SECRET_KEY = os.getenv("SECRET_KEY", "형의_비밀키")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30