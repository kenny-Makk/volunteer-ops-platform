from sqlalchemy import Boolean,String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Permission(Base):
    __tablename__="permissions"

    id: Mapped[int] =mapped_column(primary_key=True)
    name: Mapped[str] =mapped_column(String(50), unique=True)
    sensitive: Mapped[bool] = mapped_column(Boolean)
