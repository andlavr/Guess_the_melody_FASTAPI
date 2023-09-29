import traceback

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Score, Songs, Bands
from crud.song import get_songs



async def get_song_score(band, song_name, session: AsyncSession) -> list:
    """
    Получение результатов по конкретной песни

    :param session:
    :return:
    """

    try:
        song_id = await session.execute(
            select(
                Songs.id
            ).join(
                Bands
            ).filter(Songs.song_name==song_name, Bands.band_name==band)
        )

        result = song_id.fetchone()
        if result:
            song_id = result[0]

        scores = await session.execute(
            select(
                Score.name, Score.time
            ).filter(
                Score.songs_id == song_id
            )
        )

        result = scores.fetchall()
        return [(user[0], user[1]) for user in result]

    except Exception:
        traceback.print_exc()


async def post_song_score(username, song_name, band, time, session: AsyncSession) -> bool:
    """
    Запрос на сохранение данных в БД
    :param username: str
    :param song_name: dtr
    :param band: dtr
    :param time: float
    :param session:
    :return: bool
    """

    song_id = await session.execute(
        select(
            Songs.id
        ).join(
            Bands
        ).filter(Songs.song_name == song_name, Bands.band_name == band)
    )

    result = song_id.fetchone()
    if result:
        song_id = result[0]

    result = await session.execute(
        insert(
            Score
        ).values(
            songs_id=song_id, name=username, time=time
        )
    )

    await session.commit()

    return result





