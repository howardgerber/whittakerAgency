from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserProfile
from app.core.security import hash_password, verify_password, create_access_token
from app.services.audit_log_service import AuditLogService


class AuthService:
    """Business logic for authentication"""

    @staticmethod
    async def register_user(db: Session, user_data: UserRegister) -> UserProfile:
        """Register a new user with business logic and validation"""

        # Business rule: Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Audit log
        await AuditLogService.log_user_action(
            db=db,
            user_id=new_user.id,
            action="user_registered",
            entity_type="user",
            entity_id=new_user.id,
            details=f"User registered: {new_user.email}"
        )

        return UserProfile.model_validate(new_user)

    @staticmethod
    async def login_user(db: Session, credentials: UserLogin) -> Token:
        """Authenticate user and return JWT token"""

        # Find user
        user = db.query(User).filter(User.email == credentials.email).first()

        # Verify credentials
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.id)})

        # Audit log
        await AuditLogService.log_user_action(
            db=db,
            user_id=user.id,
            action="user_login",
            entity_type="user",
            entity_id=user.id,
            details=f"User logged in: {user.email}"
        )

        return Token(access_token=access_token, token_type="bearer")
