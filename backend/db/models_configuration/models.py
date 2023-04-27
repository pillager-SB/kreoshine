# pylint: disable=C0114,E1102,R0903, E0213
from __future__ import annotations
import datetime
import enum
from typing import Literal
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
import sqlalchemy

Status = Literal["received", "discussed", "in progress", "closed"]
VStatus = Literal["visible", "invsible"]


class Base(DeclarativeBase):
    """
    Базовый класс для модели
    """
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), default=datetime.datetime.now())


class ImageGroups(Base):
    """
    Таблица групп изображений
    """
    __tablename__ = "imagegroups"
    name: Mapped[str] = mapped_column(
        primary_key=True, nullable=False, unique=True)
    url_group: Mapped[list[str]] = mapped_column(ARRAY(String))


class Service(Base):
    """
    Таблица услуг.
    """
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_deskription: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[VStatus] = mapped_column(sqlalchemy.Enum(
        "visible", "invsible", name="vstatus_enum"))
    img_grop: Mapped[str] = mapped_column(ForeignKey("imagegroups.name"))


class Users(Base):
    """
    Таблица пользователей/админов базы.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    mail: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str]


class ClientRequest(Base):
    """
    Таблица карточек клиента.
    """
    __tablename__ = "client_request"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    mail: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    theme: Mapped[int] = mapped_column(ForeignKey("service.id"))
    executor: Mapped[int] = mapped_column(ForeignKey("users.id"), default=1)
    status: Mapped[Status] = mapped_column(sqlalchemy.Enum(
        "received", "discussed", "in progress", "closed", name="status_enum"))


class News(Base):
    """
    Таблица новостей.
    """
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[VStatus] = mapped_column(sqlalchemy.Enum(
        "visible", "invsible", name="vstatus_enum"))
    img_grop: Mapped[str] = mapped_column(ForeignKey("imagegroups.name"))


if __name__ == "__main__":
    pass
