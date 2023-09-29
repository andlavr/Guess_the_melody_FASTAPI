import os

import dotenv
from fastapi import FastAPI

from crud.databases import create_tables
from routes import song
from routes import score
from routes import style

dotenv.load_dotenv()

app = FastAPI()

app.include_router(song.router)
app.include_router(style.router)
app.include_router(score.router)

URI = os.getenv("URI")


@app.on_event("startup")
async def startup_db():
    await create_tables()


@app.get('/')
async def index():
    return {"HELLO": "WORLD"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8091)
