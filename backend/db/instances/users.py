from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.tables.users import User
from core.password_hashing import Hasher


def create_new_user(user:UserCreate,db:Session):
    user = User(username=user.username,
        email = user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_admin=False
        )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_id(id: int,db: Session):
    existing_user = db.query(User).filter(User.id == id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1

def list_user(id: int, db: Session):
    seance = db.query(User).filter(User.id == id).first()
    return seance