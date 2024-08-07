from typing import List
import logging
import datetime

from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, MappedAsDataclass, sessionmaker
from sqlalchemy import create_engine, ForeignKey, BigInteger, JSON

from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine import URL

from .config import DATABASE

class Base(DeclarativeBase):
    pass


class FSMRecord(Base, MappedAsDataclass):
    __tablename__ = "aiogram_fsm"
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state: Mapped[str | None]
    data: Mapped[dict[str, any]] = mapped_column(type_=JSON, default=dict())


engine = create_engine(URL.create(**DATABASE), pool_size=10, max_overflow=30)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)