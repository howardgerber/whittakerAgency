from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import UserRegister, UserLogin, Token, UserProfile
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    Thin controller - business logic in AuthService
    """
    user = await AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT token

    Thin controller - business logic in AuthService
    """
    token = await AuthService.login_user(db, credentials)
    return token


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile

    Protected endpoint requiring valid JWT
    """
    return UserProfile.model_validate(current_user)
