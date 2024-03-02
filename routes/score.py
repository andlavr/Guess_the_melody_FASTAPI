import os
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud.score as score
from crud.databases import get_session

router = APIRouter(prefix='/score', tags=['score'])


@router.get("/")
async def get_score(band: str, song_name: str, session: AsyncSession = Depends(get_session)) -> Optional[list]:
    result = await score.GET.score(band, song_name, session)

    return result


@router.post("/")
async def add_score(
        username: str, song_name: str, band: str, time: float, session: AsyncSession = Depends(get_session)
) -> bool:

    result = await score.POST.song_score(username, song_name, band, time, session)
    return True if result else False
