import os

import dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from crud.databases import create_tables
from routes import song
from routes import score
from routes import style
from routes import bands

dotenv.load_dotenv()

app = FastAPI()

app.include_router(song.router)
app.include_router(style.router)
app.include_router(score.router)
app.include_router(bands.router)

URI = os.getenv("URI")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db():
    await create_tables()


@app.get('/')
async def index():
    return {"HELLO": "WORLD"}


if __name__ == "__main__":
    import uvicorn

    env_host = os.getenv("HOST")

    uvicorn.run(app, host=env_host if env_host else "localhost", port=25001)
