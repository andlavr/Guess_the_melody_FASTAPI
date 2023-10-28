from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Style


class GET:

    @staticmethod
    async def styles(session: AsyncSession) -> list:
        """
        Получение id всех стилей

        :param session: объект типа session
        :return: объект типа id
        """
        styles = await session.execute(select(Style.style, Style.description, Style.image))
        data = styles.fetchall()

        if data:
            data = [(style[0], style[1], style[2]) for style in data]

        return data

    @staticmethod
    async def style_id(style: str, session: AsyncSession) -> Optional[int]:
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


class PUT:
    """
    Методы добавления объектов (description, image) в БД
    """
    @staticmethod
    async def description(style, description, session: AsyncSession) -> bool:
        await session.execute(update(Style).values(description=description).where(Style.style == style))
        await session.commit()
        return True

    @staticmethod
    async def image(style, image, session: AsyncSession) -> bool:
        await session.execute(update(Style).values(image=image).where(Style.style == style))
        await session.commit()
        return True
