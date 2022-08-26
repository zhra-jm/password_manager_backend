import logging
from typing import Dict, List
from fastapi import Response
import uvicorn as uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from source import crud, models, schemas
from source.database import SessionLocal, engine
from source.password_encryption import encryption
# don't remove
from source.log import LogHandler

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Password Manager",
    description="This is Password Manager Service",
    version="0.1.0",
    docs_url="/docs/",
    redoc_url="/redoc/",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/master/create/", response_model=Dict)
def create_master_password(
        password: schemas.MasterPasswordCreate,
        response: Response,
        db: Session = Depends(get_db)
):
    db_master_password = crud.create_master_password(db=db, master_password=password)
    if db_master_password:
        response.status_code = 200
        return {"message": "Master password set succuessfully"}
    raise HTTPException(status_code=400, detail={"error": "Master password doesn't set"})


@app.get('/master/check/', response_model=Dict)
def check_master_password(
        master_password: str,
        response: Response,
        db: Session = Depends(get_db)
):
    db_master = crud.check_master_password(password=master_password, db=db)
    if not db_master:
        raise HTTPException(status_code=404, detail="Password doesn't match!")
    response.status_code = 200
    return {"message": "You logged in succuessfully"}


@app.get("/master/hint/", response_model=Dict)
def get_master_password_hint(response: Response, db: Session = Depends(get_db)):
    db_master_password = crud.get_hint(db=db)
    if db_master_password is None:
        raise HTTPException(status_code=404, detail="Hint doesn't exist")
    response.status_code = 200
    return {"message": db_master_password.hint}


@app.get("/master/exist/", response_model=bool)
def check_master_password_existence(db: Session = Depends(get_db)):
    db_master_password = crud.check_master_existence(db=db)
    if db_master_password is None:
        return False
    return True


@app.post("/password/create/", response_model=Dict)
def create_password(
        password: schemas.PasswordCreate,
        response: Response,
        db: Session = Depends(get_db)):
    db_password = crud.create_password(db=db, password_data=password)
    if db_password:
        response.status_code = 200
        return {"message": "Password set succuessfully"}
    raise HTTPException(status_code=400, detail={"error": "Password doesn't set"})


@app.get("/password/all", response_model=List)
def get_all_passwords(
        response: Response,
        db: Session = Depends(get_db)
):
    passwords = crud.get_all_password(db=db)
    if passwords:
        response.status_code = 200
        return passwords
    response.status_code = 200
    return []


@app.get("/password/find/", response_model=Dict)
def get_password_by_name(name: str, response: Response, db: Session = Depends(get_db)):
    password = crud.get_password_by_name(db=db, name=name)
    if password:
        response.status_code = 200
        return {"message": password}
    raise HTTPException(status_code=400, detail={"error": "Password doesn't found"})


@app.put("/password/edit/", response_model=Dict)
def edit_password(password_id: int, password: schemas.PasswordCreate, response: Response,
                  db: Session = Depends(get_db)):
    database_password = crud.update_password_by_id(db=db, password_id=password_id, password=password)
    if database_password:
        response.status_code = 200
        return {"message": "Password edited succuessfully"}
    else:
        raise HTTPException(status_code=400, detail={"error": "Password doesn't found"})


@app.get("/password/show/", response_model=Dict)
def show_password(password_id: int, response: Response, db: Session = Depends(get_db)):
    password = crud.get_password_by_id(db=db, password_id=password_id)
    if password:
        response.status_code = 200
        return {"message": password}
    else:
        raise HTTPException(status_code=400, detail={"error": "Password doesn't found"})


@app.delete("/password/delete/", response_model=Dict)
def delete_password(password_id: int, response: Response, db: Session = Depends(get_db)):
    password = crud.delete_password_by_id(db=db, password_id=password_id)
    if password:
        response.status_code = 200
        return {"message": "Password deleted succuessfully"}
    else:
        raise HTTPException(status_code=400, detail={"error": "Password doesn't found"})


@app.post("/password/password_creator/", response_model=Dict)
def password_creator(
        response: Response,
        length: int = 12,
        upper: bool = True,
        lower: bool = True,
        digit: bool = True,
        pun: bool = True,
):
    try:
        message = encryption.create_password(length=length, upper=upper, lower=lower, digit=digit, pun=pun)
        response.status_code = 200
        return {"message": message}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail={"error": "Can't create password"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
