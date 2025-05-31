from . import Base
from sqlalchemy.orm import Mapped, mapped_column

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default="")