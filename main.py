import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.teas import router as TeasRouter
from controllers.comments import router as CommentsRouter
from controllers.users import router as UsersRouter


tags_metadata = [
    {
        "name": "User Managment",
        "description": "this is the main dashboard to manage users for login and logout"
    },
    {
        "name": "Tea Managment",
        "description": "this is the main dashboard to manage users teas they havce chosen"
    },
    {
        "name": "Review Managment",
        "description": "this is the main dashboard to manage the reviews for individual teas"
    }
]


app = FastAPI(
    title="My favourite Tea app, keep track of all the teas in the world",
    description="only the cool kids know how to make the best chai",
    version="1.2.0",
    openapi_tags=tags_metadata
)


origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(TeasRouter, prefix="/api")
app.include_router(CommentsRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")


@app.get("/")
def home():
    return {"message": "Home Page"}