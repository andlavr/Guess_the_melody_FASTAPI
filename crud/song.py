import random
import traceback

from sqlalchemy import select, func, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from crud import style as crud_style
from crud.models import Songs, Bands


class GET:

    @staticmethod
    async def random_songs(session: AsyncSession) -> Songs:
        """
        Получение всех записей из таблицы Songs

        :param session: объект сессии для подключения к БД

        :return: рандомная песня
        """

        try:
            songs = await session.execute(select(Songs.style_id, Songs.band_id, Songs.song_name))
            all_songs = songs.fetchall()

            random_song = random.choice(all_songs)

            song = await session.execute(
                select(
                    Bands.band_name, Songs.song_name, Songs.song_text, Songs.data_ogg
                ).join(
                    Bands
                ).filter(
                    Songs.style_id == random_song[0], Songs.band_id == random_song[1], Songs.song_name == random_song[2]
                )
            )

            result = song.fetchone()

            return result  # Конвертация объектов типа Row в объект SQLAlchemy

        except Exception:
            traceback.print_exc()

    @staticmethod
    async def random_song_by_style(style: str, session: AsyncSession):
        """
        Получение случайной песни по стилю

        :param style: стиль песни
        :param session: объект сессии для подключения к БД

        :return: песня
        """

        my_style_id = await crud_style.GET.style_id(style, session)

        if not my_style_id:
            return None

        song = await session.execute(
            select(
                Songs.style_id, Songs.band_id, Songs.song_name
            ).filter_by(
                style_id=my_style_id
            )
        )

        result = song.fetchall()
        if result:
            random_song = random.choice(result)

            song = await session.execute(
                select(
                    Bands.band_name, Songs.song_name, Songs.song_text, Songs.data_ogg
                ).join(
                    Bands
                ).filter(
                    Songs.style_id == random_song[0], Songs.band_id == random_song[1], Songs.song_name == random_song[2]
                )
            )

            result = song.fetchone()
            return result

        return None

    @staticmethod
    async def random_label(session):
        """
        Получение названия случайной песен

        :param session: объект сессии для подключения к БД

        :return: название песни
        """

        song_count = await session.execute(func.count(Songs.song_name))
        song_count = song_count.scalars().one()

        song = await session.execute(
            select(
                Bands.band_name, Songs.song_name
            ).join(
                Bands
            ).limit(1).offset(random.randint(0, song_count - 1))
        )

        result = song.fetchall()
        if result:
            result = [f"{song[0]} - {song[1]}" for song in result]
        return result

class POST:

    @staticmethod
    async def song(session: AsyncSession, style_id: int, band_id: int, song_name: str, song_text: str, data_ogg: bytes):
        """
        Добавление песни в БД

        :param session: объект сессии для подключения к БД
        :param style_id: id стиля
        :param band_id: id группы
        :param song_name: название песни
        :param song_text: слова песни

        :return: dict
        """

        try:
            await session.execute(insert(Songs).values(style_id=style_id, band_id=band_id, song_name=song_name, song_text=song_text, data_ogg=data_ogg))
            await session.commit()

            return {'result': True, "message": "Song added"}
        except IntegrityError:
            traceback.print_exc()
            return {"result": False, "message": "Song already exists"}
