import os
import typing

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Bands


class GET:
    @staticmethod
    async def band_id(session: AsyncSession, band_name: str) -> typing.Union[int]:
        """
        Получение id группы

        :param band_name: название группы
        :return: id группы
        """

        band_id = session.query(Bands).filter_by(band_name=band_name).first()
        return band_id.id

    @staticmethod
    async def band(session: AsyncSession, band_name: str):
        """
        Получение id группы

        :param band_name: название группы
        :return: id группы
        """

        try:

            styles = await session.execute(select(Bands).filter_by(band_name=band_name))
            data = styles.mappings().one()

            if data:
                return data["Bands"]
            return None
        except NoResultFound:
            return None


class POST:
    @staticmethod
    async def band(session: AsyncSession, band_name):
        """
        Добавление названия группы в БД

        :param band_name: название группы
        :token: объект типа str
        :return: bool
        """

        try:
            await session.execute(
                insert(
                    Bands
                ).values(
                    band_name=band_name
                )
            )

            await session.commit()
            return {"result": True, "message": "Ok"}
        except IntegrityError:
            return {"result": False, "message": "Band already exists"}
