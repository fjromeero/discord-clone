from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models.base import User 

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    print({"DB INITIALIZED"})