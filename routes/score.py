import json
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import crud.score as score
from crud.databases import get_session
from crud.models import Songs
from schemes.song import Song

router = APIRouter()


@router.get("/score/")
async def random_song(band: str, song_name: str, session: AsyncSession = Depends(get_session)) -> Optional[list]:
    result = await score.get_song_score(band, song_name, session)

    return result


@router.post("/score/")
async def random_song(
        username: str, song_name: str, band: str, time: float, session: AsyncSession = Depends(get_session)
) -> bool:

    result = await score.post_song_score(username, song_name, band, time, session)
    return True if result else False
