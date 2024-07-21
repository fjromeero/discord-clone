from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create, update={
            "hashed_password": get_password_hash(user_create.password)
        }
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    query = select(User).where(User.email == email)
    db_user = session.exec(query).first()
    return db_user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    query = select(User).where(User.username == username)
    db_user = session.exec(query).first()
    return db_user


def get_user_by_display_name(*, session: Session, display_name: str) -> User | None:
    query = select(User).where(User.display_name == display_name)
    db_user = session.exec(query).first()
    return db_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)

    if not db_user or not verify_password(plain_password=password, hashed_password=db_user.hashed_password):
        return None

    return db_user


def update_user_password(*, session: Session, user: User, password: str):
    hashed_password = get_password_hash(password=password)
    user.hashed_password=hashed_password
    session.add(user)
    session.commit()

