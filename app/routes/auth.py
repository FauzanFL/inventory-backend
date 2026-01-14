from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.crud import user as crud_user
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data : OAuth2PasswordRequestForm = Depends()
):
    user = crud_user.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.username, role=user.role.name)
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}