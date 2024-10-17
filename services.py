# services.py
from typing import Set
from sqlalchemy.orm import Session
import models
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from auth import create_access_token
from schemas import RegisteredUserCreate, RegisteredUserResponse, User
import httpx

class UserService:
    def __init__(self, db: Session):
        self.db = db

    # In-memory set to store blacklisted tokens
    blacklisted_tokens: Set[str] = set()

    

    def register_user(self, Ruser: RegisteredUserCreate) -> RegisteredUserResponse:
        hashed_password = bcrypt.hashpw(Ruser.password.encode('utf-8'), bcrypt.gensalt())
        new_user = models.RegisteredUser(
            name=Ruser.name,
            hashed_password=hashed_password.decode('utf-8')
        )
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except SQLAlchemyError as e:
            self.db.rollback()  # Rollback in case of failure
            print(f"Error registering user: {str(e)}")
            raise

        return new_user

    def get_all_registered_users(self) -> list[RegisteredUserResponse]:
        try:
            return self.db.query(models.RegisteredUser).all()
        except SQLAlchemyError as e:
            print(f"Error fetching users: {str(e)}")
            raise

    def login(self, username: str, password: str) -> str:
        try:
            user = self.db.query(models.RegisteredUser).filter(models.RegisteredUser.name == username).first()
        except SQLAlchemyError as e:
            print(f"Error during login: {str(e)}")
            raise

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return None
        return create_access_token(data={"sub": user.name})

    def logout(self, token: str):
        try:
            self.blacklisted_tokens.add(token)
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            raise

    def is_token_blacklisted(self, token: str) -> bool:
        return token in self.blacklisted_tokens

    def get_all_users(self) -> list[User]:
        try:
            return self.db.query(models.User).all()
        except SQLAlchemyError as e:
            print(f"Error fetching users: {str(e)}")
            raise

    def add_user(self, user: User) -> User:
        try:
            existing_user = self.db.query(models.User).filter(models.User.id == user.id).first()
            if existing_user:
                return None

            new_user = models.User(
                id=user.id,
                name=user.name,
                city=user.city,
                isMale=user.isMale
            )
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error adding user: {str(e)}")
            raise

    def update_user(self, user_id: int, user: User) -> User:
        try:
            existing_user = self.db.query(models.User).filter(models.User.id == user_id).first()
            if not existing_user:
                return None
            existing_user.name = user.name
            existing_user.city = user.city
            existing_user.isMale = user.isMale
            self.db.commit()
            return existing_user
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error updating user: {str(e)}")
            raise

    def delete_user(self, user_id: int) -> User:
        try:
            existing_user = self.db.query(models.User).filter(models.User.id == user_id).first()
            if not existing_user:
                return None
            self.db.delete(existing_user)
            self.db.commit()
            return existing_user
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error deleting user: {str(e)}")
            raise

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return self.db.query(models.User).filter(models.User.id == user_id).first()
        except SQLAlchemyError as e:
            print(f"Error fetching user by ID: {str(e)}")
            raise
