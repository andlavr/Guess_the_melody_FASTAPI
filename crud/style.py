import os
from typing import Optional

from sqlalchemy import select, update, insert
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Style


class GET:

    @staticmethod
    async def styles(session: AsyncSession) -> list:
        """
        Получение id всех стилей

        :param session: объект типа session

        :return: id стиля
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

        :param style: название стиля
        :param session: объект сессии session

        :return: id стиля или None
        """

        styles = await session.execute(select(Style.id).filter_by(style=style))
        data = styles.fetchone()

        if data:
            return data[0]
        return data

    @staticmethod
    async def style(style_name: str, session: AsyncSession) -> Optional[int]:
        """
        Получение id стиля из БД

        :param style: название стиля
        :param session: объект сессии session

        :return: id стиля или None
        """
        try:

            styles = await session.execute(select(Style).filter_by(style=style_name))
            data = styles.mappings().one()

            if data:
                return data["Style"]
            return None
        except NoResultFound:
            return None


class POST:
    @staticmethod
    async def style(session: AsyncSession, style: str, image: bytes = None, description: str = None):
        """
        Добавляет стиль в БД

        :param style: название стиля
        :return: bool
        """

        try:
            await session.execute(insert(Style).values(style=style, image=image, description=description))
            await session.commit()

            return {'result': True, "message": "Style added"}
        except IntegrityError:
            return {"result": False, "message": "Style already exists"}


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
