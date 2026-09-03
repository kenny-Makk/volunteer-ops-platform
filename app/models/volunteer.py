from sqlalchemy import String, ForeignKey,Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, func


class Volunteer(Base):
    __tablename__="volunteers"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[Optional[int]] =mapped_column(ForeignKey("assessments.id"),unique=True)
    name: Mapped[str] = mapped_column(String(100))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    membership_tier_id: Mapped[int]=mapped_column(ForeignKey("membership_tiers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))