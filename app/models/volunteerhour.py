from typing import Optional
from sqlalchemy import String,Integer,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class VolunteerHour(Base):
    __tablename__="volunteer_hours"

    id: Mapped[int] = mapped_column(primary_key=True)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("volunteers.id"))
    event_name: Mapped[str] = mapped_column(String(50))
    supervisor_name: Mapped[str]=mapped_column(String(40))
    organisation_name:Mapped[str] =mapped_column(String(50))
    evidence_form: Mapped[str]=mapped_column(String(200))
    task_summary: Mapped[str]=mapped_column(String(500))
    hours: Mapped[int]=mapped_column(Integer)
    minutes: Mapped[int]=mapped_column(Integer)
    status: Mapped[str]=mapped_column(String(20), default="pending")
    approved_by:Mapped[Optional[int]]=mapped_column(ForeignKey("users.id"))
