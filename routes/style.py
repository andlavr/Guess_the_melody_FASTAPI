import base64
import os

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from crud import style as crud_style
from crud.databases import get_session

router = APIRouter()

@router.get("/styles/")
async def songs(session: AsyncSession = Depends(get_session)) -> list:
    result = await crud_style.GET.styles(session)

    return result

@router.put("/styles/description/")
async def update_songs_description(style: str, description: str, token: str, session: AsyncSession = Depends(get_session)) -> bool:
    if token != os.getenv("TOKEN"):
        return False
    result = await crud_style.PUT.description(style, description, session)
    return result

@router.put("/styles/image/")
async def update_songs_image(style: str, token: str, image: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    if token != os.getenv("TOKEN"):
        return False

    result = await crud_style.PUT.image(style, base64.b64encode(image.file.read()), session)
    image.file.close()
    return result