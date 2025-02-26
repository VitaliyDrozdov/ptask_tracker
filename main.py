from fastapi import FastAPI

from handlers import routers

app = FastAPI()
app.mount("/api", app)


for router in routers:
    app.include_router(router)
