from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud.models import Style


async def get_all_styles(session: AsyncSession) -> list:
    """
    Получение id всех стилей

    :param session: объект типа session
    :return: объект типа id
    """
    styles = await session.execute(select(Style.style, Style.description))
    data = styles.fetchall()

    if data:
        data = [(style[0], style[1]) for style in data]

    return data



async def get_style_id(style: str, session: AsyncSession) -> Optional[int]:
    """
    Получение id стиля из БД


    :param style: объект типа str
    :param session: объект сессии session
    :return: id стиля или None
    """

    styles = await session.execute(select(Style.id).filter_by(style=style))
    data = styles.fetchone()

    if data:
        return data[0]
    return data
