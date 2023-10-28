import random
import traceback

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from crud import style as crud_style
from crud.models import Songs, Bands


# def add_song(style_id: int, band_id: int, song_name: str, song_text: str) -> None:
#     """
#     Добавление песен в БД
#
#     :param style_id: объект типа int
#     :param band_id: объект типа int
#     :param song_name: объект типа str
#     :param song_text: объект типа str
#     :return: None
#     """
#
#     new_song = Songs(style_id=style_id, band_id=band_id, song_name=song_name, song_text=song_text)
#
#     session.add(new_song)
#
#     session.commit()


async def get_songs(session: AsyncSession) -> list:
    """
    Получение id всех песен

    :return:объект типа id
    """

    songs = await session.execute(select(Songs.style_id, Songs.band_id, Songs.song_name))
    data = songs.fetchall()
    return data


async def get_random_songs(session: AsyncSession) -> Songs:
    """
    Получение всех записей из таблицы Songs

    :param session:
    :return:
    """

    try:
        all_songs = await get_songs(session)
        random_song = random.choice(all_songs)

        # TODO: Подумать над рефактором
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


async def get_random_song_by_style(style: str, session: AsyncSession):
    """
    Получение случайной песни по стилю

    :param style:
    :param session:
    :return:
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

        # TODO: Подумать над рефактором
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


async def get_random_label(session):
    """
    Получение названия случайной песен
    :param session:
    :return:
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
