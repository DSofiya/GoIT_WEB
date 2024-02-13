from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(150))
    phone_number: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[str] = mapped_column(String(30))
    data: Mapped[bool] = mapped_column(default=False, nullable=True)
