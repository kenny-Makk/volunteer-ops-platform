from sqlalchemy import ForeignKey,Boolean,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Attendance(Base):
    __tablename__="attendances"
    __table_args__ = (UniqueConstraint("event_id", "volunteer_id"),)


    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("volunteers.id"))
    registered: Mapped[bool]=mapped_column(Boolean)
    attended: Mapped[bool]=mapped_column(Boolean)
    certificate_issued: Mapped[bool]=mapped_column(Boolean)