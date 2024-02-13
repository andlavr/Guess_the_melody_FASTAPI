from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud.song as song
from crud.databases import get_session
from schemes.song import Song

router = APIRouter()


@router.get("/random_song/")
async def random_song(style: Optional[str] = None, session: AsyncSession = Depends(get_session)) -> Optional[Song]:
    if style is None:
        result = await song.get_random_songs(session)
    else:
        result = await song.get_random_song_by_style(style, session)

    return result


@router.get("/random_label/")
async def wrong_answer(session: AsyncSession = Depends(get_session)) -> list:
    result = await song.get_random_label(session)

    return result
