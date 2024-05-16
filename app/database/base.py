from sqlalchemy.orm import DeclarativeBase

from app.database.meta import meta


class Base(DeclarativeBase):
    metadata = meta
