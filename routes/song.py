import base64
import os
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

import crud.song as song
from crud.databases import get_session
from schemes.song import Song

router = APIRouter(prefix='/song', tags=['song'])


@router.get("/random/")
async def random_song(style: Optional[str] = None, session: AsyncSession = Depends(get_session)) -> Optional[Song]:
    if style is None:
        result = await song.GET.random_songs(session)
    else:
        result = await song.GET.random_song_by_style(style, session)

    return result


@router.get("/random_label/")
async def wrong_answer(session: AsyncSession = Depends(get_session)) -> list:
    result = await song.GET.random_label(session)

    return result


@router.post('/')
async def add_song(
        token: str,
        style_id: int,
        band_id: int,
        song_name: str,
        song_text: str,
        ogg_file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    if token != os.getenv("TOKEN"):
        return {"result": False, "message": "Token is invalid"}
    print("ok")
    try:
        if not ogg_file.filename.endswith('.ogg'):
            return {'result': False, "message": "Wrong file format. File is not .ogg"}

        contents = base64.b64encode(ogg_file.file.read())
    except Exception as err:
        return {'result': False, "message": err}
    finally:
        ogg_file.file.close()

    result = await song.POST.song(session, style_id, band_id, song_name, song_text, contents)

    return result
#