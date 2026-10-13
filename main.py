from fastapi import FastAPI
from routers import router
from setup import init_tables

app = FastAPI()
app.include_router(router)

init_tables()  # Initialize the database tables when the application starts

