from fastapi import FastAPI

from api.routes import health


app = FastAPI(
    title="FastAPI Example",
)

app.include_router(health.router)
