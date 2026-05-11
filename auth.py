from passlib.context import CryptContext
from jose import jwt , JWTError
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from datetime import datetime , timedelta
from fastapi import Depends , status , HTTPException
from dotenv import load_dotenv
import os 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwt_context = CryptContext(schemes=["bcrypt"])
security_bearer = HTTPBearer()

def hash_password(password:str):
    return pwt_context.hash(password)

def varify_password(plain_password , hashed_password):
    return pwt_context.verify(plain_password,hashed_password)

def create_token(email:str):
    now  = datetime.now()
    expire = now + timedelta(minutes=30)
    payload = {
        "sub" : email,
        "exp" : expire

    }
    token  = jwt.encode(payload , SECRET_KEY , algorithm=ALGORITHM)
    return token

def verify_token(token : HTTPAuthorizationCredentials = Depends(security_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not valid credential",
        headers={"www-Authenticate":"Bearer"}
    )
    try :
        payload = jwt.decode(token.credentials , SECRET_KEY , algorithms=[ALGORITHM])
        email : str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError :
        raise credentials_exception
    return email    

