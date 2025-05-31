from sqlalchemy import Column, ForeignKey, Label, Table
from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Label(Base):
    __tablename__ = "label"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=True, default="")
    color: Mapped[str] = mapped_column(default="blue")

association_task_label = Table(
    "association_task_label",
    Base.metadata,
    Column("task_id", ForeignKey("task.id")),
    Column("label_id", ForeignKey("label.id"))
)

class Task(Base):
    __tablename__ = "task"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default="")
    labels: Mapped[list[Label]] = relationship(secondary=association_task_label, lazy="selectin")


