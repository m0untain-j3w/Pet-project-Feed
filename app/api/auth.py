from fastapi import APIRouter

from api.dependencies.backend import authentication_backend
from api.dependencies.fastapi_users_conf import fastapi_users
from core.config import settings
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)
# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
)

# register/
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

# /request-verify
# /verify
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

# /reset-password-request
# /reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
)