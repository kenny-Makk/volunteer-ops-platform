# Import every model here so Alembic's autogenerate (env.py) can see them
# via Base.metadata. Add a line for each new model as you write it.
from app.models.application import Application  # noqa: F401
from app.models.assessment import Assessment  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.membershiptier import MembershipTier  # noqa: F401
