import os

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud.bands as bands
from crud.databases import get_session

router = APIRouter(prefix='/band', tags=['band'])


@router.get("/")
async def get_band(band_name: str, session: AsyncSession = Depends(get_session)):

    result = await bands.GET.band(session, band_name)
    return result

@router.post("/")
async def add_band(band_name: str, token: str, session: AsyncSession = Depends(get_session)):
    if token != os.getenv("TOKEN"):
        return {"result": False, "message": "Token is invalid"}

    result = await bands.POST.band(session, band_name)
    return result



