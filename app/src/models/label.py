from sqlalchemy import Column, ForeignKey, Table
from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Label(Base):
    __tablename__ = "label"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=True, default="")