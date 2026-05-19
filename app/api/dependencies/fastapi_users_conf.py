from core.models import User
from fastapi_users import FastAPIUsers
from .backend import authentication_backend

from .user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)