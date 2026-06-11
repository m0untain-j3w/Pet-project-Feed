from app.core.models import User
from fastapi_users import FastAPIUsers
from app.api.dependencies.backend import authentication_backend

from app.api.dependencies.user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)