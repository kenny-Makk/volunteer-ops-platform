from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    """Fields shared by every Application schema."""

    applicant_name: str


class ApplicationCreate(ApplicationBase):
    """What a client sends to submit a new application (POST body).

    Deliberately excludes id/status/submitted_at — those are server-
    controlled, not client-supplied.
    """

    pass


class ApplicationRead(ApplicationBase):
    """What the API returns to a client (response model).

    from_attributes=True lets this be built directly from a SQLAlchemy
    Application instance (model_validate(db_application)), not just a dict.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    submitted_at: datetime
