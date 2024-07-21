from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.core import security
from app.crud import user as UserCrud
from app.models.user import UserCreate, ResetUserPassword
from app.models.token import Token
from app.models.message import Message
from app.utils import mail as MailService

router = APIRouter()


@router.post('/register')
def register(
    session: SessionDep,
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    
    user = UserCrud.get_user_by_email(session=session, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email alredy exists in the system.",
        )
    
    user = UserCrud.get_user_by_username(session=session, username=user_in.username)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username alredy exists in the system.",
        )
    
    user = UserCrud.get_user_by_display_name(session=session, display_name=user_in.display_name)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user witht this display name alredy exists in the system.",
        )
    
    user = UserCrud.create_user(session=session, user_create=user_in)


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = UserCrud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Login or password is invalid"
        )
    
    return Token(
        access_token=security.create_access_token(
            subject=user.email
        )
    )


@router.post("/auth/forgot")
def forgot_password(
    session: SessionDep, email: str
) -> Message:
    """
    Send password recovery email to the user
    """
    user = UserCrud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email does not exist"
        )

    password_reset_token = security.generate_password_reset_token(email=email)
    email_data = MailService.generate_reset_password_email(
        email_to=email,
        username=user.username,
        token=password_reset_token,
    )
    MailService.send_email(
        email_to=email,
        html_content=email_data.html_content,
        subject=email_data.subject,
    )

    return Message(
        message="Password recovery email has been sent"
    )


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: ResetUserPassword) -> Message:
    """
    Reset user password
    """

    email = security.verify_password_reset_token(token=body.token)

    if not email:
        raise HTTPException(status_code=404, detail="Invalid token")
    
    user = UserCrud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email does not exist"
        )
    
    UserCrud.update_user_password(session=session, user=user, password=body.new_password)

    return Message(message="Password updated successfully")
