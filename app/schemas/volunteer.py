from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class VolunteerBase(BaseModel):
    name:str

class VolunteerCreate(VolunteerBase):
    membership_tier_id: int

class VolunteerRead(VolunteerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    assessment_id: Optional[int]
    user_id: int
    membership_tier_id: int
    joined_at: datetime

    