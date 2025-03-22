from src.handlers.auth import router as auth_router
from src.handlers.category import router as category_router
from src.handlers.tasks import router as task_router
from src.handlers.user import router as user_router

routers = [task_router, category_router, auth_router, user_router]
