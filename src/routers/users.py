from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.schema_user import User
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.model.database import get_session
from src.model.model_user import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            User.email == user.email
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user