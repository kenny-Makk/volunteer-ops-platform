# Import every model here so Alembic's autogenerate (env.py) can see them
# via Base.metadata. Add a line for each new model as you write it.
from app.models.application import Application  # noqa: F401
from app.models.assessment import Assessment  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.membershiptier import MembershipTier  # noqa: F401
from app.models.volunteer import Volunteer  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.attendance import Attendance  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.permission import Permission  # noqa: F401
from app.models.userrole import UserRole  # noqa: F401
from app.models.rolepermission import RolePermission  # noqa: F401
from app.models.volunteerhour import VolunteerHour  # noqa: F401
