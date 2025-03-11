from fastapi import FastAPI

from src.handlers import routers

app = FastAPI()
app.mount("/api", app)


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
