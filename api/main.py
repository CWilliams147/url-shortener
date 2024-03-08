from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.links import Links, LinksSchema
from db import session, engine
from models.base import Base
from config import settings
from models.users import UserSchema, UserAccountSchema, User
from models.token import Token, TokenData, create_access_token
from services import create_user, get_user
from datetime import date, timedelta
from starlette.responses import RedirectResponse

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION);
    create_tables()
    return app

app = start_application()

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "Root Route"}

@app.get("/links")
def get_links():
    link = Links()
    shortUrl = session.query(Links)
    return shortUrl.all()

@app.post("/create/links")
def get_Links(url_data: LinksSchema):
    link = Links(**url_data.dict())
    session.add(link)
    session.commit()
    return link

@app.post("/register", response_model=UserSchema)
def register_user(payload: UserAccountSchema):
    payload.hashed_password = User.hash_password(payload.hashed_password)
    return create_user(user=payload)

@app.post("/login")
async def login(payload: UserAccountSchema):
    try:
        user: User = get_user(email=payload.email)
        print(user)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User Email Credentials"
        )
    
    is_validated: bool = user.validate_password(payload.hashed_password)

    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User Credentials"
        )
    access_token_expires = timedelta(minutes=120)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/sendit")
async def redirect_to_external_url(url: str = Query(...)):
    link = session.query(Links).filter(Links.short_url == url).first()
    
    long_url = f"https://{link.long_url}"

    return RedirectResponse(long_url)