import json

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import crud.style as style
from crud.databases import get_session
from crud.models import Songs
from schemes.song import Song

router = APIRouter()


@router.get("/styles/")
async def songs(session: AsyncSession = Depends(get_session)) -> list:
    result = await style.get_all_styles(session)

    return result

