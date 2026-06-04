from fastapi import FastAPI
from routers.auth_routes import router as auth_router
from routers.expenses import router as expenses_router
from routers.users import router as users_router
app = FastAPI()
app.include_router(auth_router)
app.include_router(expenses_router)
app.include_router(users_router)