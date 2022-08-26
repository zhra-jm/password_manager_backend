import logging
from sqlalchemy.orm import Session
from . import models, schemas
from .password_encryption import encryption


def create_master_password(db: Session, master_password: schemas.MasterPasswordCreate):
    try:
        existence_master = db.query(models.MasterPassword).all()
        if not existence_master:
            db_master_password = models.MasterPassword(
                master_password=encryption.password_encryption(master_password.master_password),
                hint=master_password.hint
            )
            db.add(db_master_password)
            db.commit()
            db.refresh(db_master_password)
            return db_master_password
        existence_master.master_password = master_password.master_password
        existence_master.hint = master_password.hint
        db.commit()
        db.close()
        return True
    except Exception as e:
        logging.error(e)
        return False


def check_master_password(db: Session, password: str):
    try:
        db_master_password = db.query(models.MasterPassword).first()
        res = encryption.check_password(password, db_master_password.master_password)
        return res
    except Exception as e:
        logging.error(e)
        return False


def get_hint(db: Session):
    try:
        db_master_password = db.query(models.MasterPassword).first()
        return db_master_password
    except Exception as e:
        logging.error(e)
        return False


def check_master_existence(db: Session):
    try:
        db_master_password = db.query(models.MasterPassword).first()
        return db_master_password
    except Exception as e:
        logging.error(e)
        return False


def create_password(db: Session, password_data: schemas.PasswordCreate):
    try:
        if password_data.password == "":
            password_data.password = encryption.create_password()
        db_password = models.Password(
            username=password_data.username,
            name=password_data.name,
            url=password_data.url,
            password=password_data.password
        )
        db.add(db_password)
        db.commit()
        db.refresh(db_password)
        return db_password
    except Exception as e:
        logging.error(e)
        return False


def get_all_password(db: Session):
    try:
        return db.query(models.Password).all()
    except Exception as e:
        logging.error(e)
        return False


def get_password_by_name(db: Session, name: str):
    try:
        return db.query(models.Password).filter(models.Password.name == name).all()
    except Exception as e:
        logging.error(e)
        return False


def get_password_by_id(db: Session, password_id: int):
    try:
        return db.query(models.Password).filter(models.Password.id == password_id).first()
    except Exception as e:
        logging.error(e)
        return False


def update_password_by_id(db: Session, password_id: int, password: schemas.PasswordCreate):
    try:
        database = db.query(models.Password).filter(models.Password.id == password_id).first()
        if database:
            if password.password == "":
                password.password = encryption.create_password()
            database.password = password.password
            database.username = password.username
            database.url = password.url
            database.name = password.name
            db.commit()
            db.close()
            return True
        db.commit()
        return False
    except Exception as e:
        logging.error(e)
        return False


def delete_password_by_id(db: Session, password_id: int):
    try:
        database = db.query(models.Password).filter(models.Password.id == password_id).first()
        if database:
            db.delete(database)
            db.commit()
            db.close()
            return True
        db.commit()
        return False
    except Exception as e:
        logging.error(e)
        return False
