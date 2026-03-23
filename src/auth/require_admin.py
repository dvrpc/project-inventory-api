from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os

load_dotenv()

security = HTTPBearer()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN")
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS")
ALLOWED_EMAILS = ALLOWED_EMAILS.split(',')

async def require_admin(credentials=Depends(security)):
    try:
        idinfo = id_token.verify_oauth2_token(
            credentials.credentials,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    email = idinfo.get("email")
    domain = idinfo.get("hd")

    if not email:
        raise HTTPException(status_code=401, detail="Missing email in token")

    if domain != ALLOWED_DOMAIN:
        raise HTTPException(status_code=403, detail="Forbidden: invalid domain")

    if email not in ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Forbidden: email not allowed")

    return True