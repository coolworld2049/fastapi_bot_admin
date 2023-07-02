from fastapi import APIRouter

from bot_admin_service.api.api_v1.endpoints import (
    login,
    signup,
    emails,
    verify,
    bot,
    botusers,
    posts,
)
from bot_admin_service.api.api_v1.endpoints import users

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(signup.router, prefix="/signup", tags=["signup"])
api_router.include_router(verify.router, prefix="/verify", tags=["verify"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(bot.router, prefix="/bot", tags=["telegram"])
api_router.include_router(botusers.router, prefix="/botusers", tags=["telegram"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
