# app/repositories/user_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
        
    # ========================= #
    #          CREATE           #
    # ========================= #
    def create(self, username: str) -> Optional[User]:
        user = User(username=username)
        
        try:
            self.db.add(user)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            user = self.db.query(User).filter_by(username=username).first()
        
        return user
    

    # ========================= #
    #           READ            #
    # ========================= #
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)


    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter_by(username=username).first()


    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).order_by(User.username).offset(skip).limit(limit).all()

    
    # ========================= #
    #         UPDATE            #
    # ========================= #
    def update(self, user_id: int, new_username: str) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        user.username = new_username
        self.db.flush()
       
        return user
    
    
    # ========================= #
    #          DELETE           #
    # ========================= #
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
    
        if not user:
            return False
    
        self.db.delete(user)
        self.db.flush()
    
        return True
    
    
    # ========================= #
    #        ADDITIONAL         #
    # ========================= #
    def count(self) -> int:
        return self.db.query(User).count()
    