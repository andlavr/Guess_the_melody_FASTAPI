import base64
import os

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from crud import style as crud_style
from crud.databases import get_session

router = APIRouter(prefix='/style', tags=['style'])


@router.get("/all")
async def get_styles(session: AsyncSession = Depends(get_session)) -> list:
    result = await crud_style.GET.styles(session)

    return result


@router.get("/")
async def get_styles(style_name: str, session: AsyncSession = Depends(get_session)):
    result = await crud_style.GET.style(style_name, session)

    return result


@router.post("/")
async def add_style(token: str, style_name: str, description: str, image: UploadFile = File(...),
                    session: AsyncSession = Depends(get_session)) -> dict:
    if token != os.getenv("TOKEN"):
        return {"result": False, "message": "Token is invalid"}

    result = await crud_style.POST.style(session, style_name, base64.b64encode(image.file.read()), description)

    return result


@router.put("/description/")
async def update_songs_description(style: str, description: str, token: str,
                                   session: AsyncSession = Depends(get_session)) -> bool:
    if token != os.getenv("TOKEN"):
        return False
    result = await crud_style.PUT.description(style, description, session)
    return result


@router.put("/image/")
async def update_songs_image(style: str, token: str, image: UploadFile = File(...),
                             session: AsyncSession = Depends(get_session)):
    if token != os.getenv("TOKEN"):
        return False

    result = await crud_style.PUT.image(style, base64.b64encode(image.file.read()), session)
    image.file.close()
    return result
