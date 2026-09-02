from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import Optional

class Assessment(Base):
    __tablename__="assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"),unique=True)
    result: Mapped[str]= mapped_column(String(20))
    assessed_by: Mapped[Optional[int]]=mapped_column(ForeignKey("users.id"),nullable=True)
