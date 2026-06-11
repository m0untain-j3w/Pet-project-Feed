from typing import TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from app.core.logger import setup_logging
from app.core.config import settings
from app.core.models import User

import logging

if TYPE_CHECKING:
    from fastapi import Request

setup_logging()
log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: "Request | None" = None,
    ):
        log.warning(
            f"User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: "Request | None" = None,
    ):
        log.warning(
            f"Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: "Request | None" = None,
    ):
        log.warning(
            f"User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
