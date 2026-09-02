
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MembershipTier(Base):
    __tablename__="membership_tiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50),unique=True)
    required_hours: Mapped[int] = mapped_column(Integer)