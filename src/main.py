from fastapi import FastAPI

from src.api.routes import health


app = FastAPI(
    title="FastAPI Example",
)

app.include_router(health.router)
