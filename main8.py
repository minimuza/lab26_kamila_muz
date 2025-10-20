from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal # функция подключения к БД

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "Пользователь зарегистрирован"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return {"error": "Неверные данные"}
    return {"msg": "Успешный вход"}

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
 to_encode = data.copy()
 expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
 to_encode.update({"exp": expire})
 encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
 return encoded_jwt

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
 user = db.query(User).filter(User.username == username).first()
 if not user or not verify_password(password, user.password_hash):
    return {"error": "Неверные данные"}
    token = create_access_token({"sub": user.username})
 return {"access_token": token, "token_type": "bearer"}

from fastapi import Header, HTTPException

def get_current_user(token: str = Header(...)):
 try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    return username
 except JWTError:
    raise HTTPException(status_code=401, detail="Ошибка проверки токена")

@app.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
 return {"user": current_user}