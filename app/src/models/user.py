from src.models.task import Task
from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)

    nom: Mapped[str] = mapped_column(index=True)
    prenom: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list[Task]] = relationship(back_populates="user")