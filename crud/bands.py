import typing

from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Bands


def get_band_id(session: AsyncSession, band_name: str) -> typing.Union[int]:
    """
    Получение id  группы

    :param band_name: объект типа str
    :return: объект типа int
    """

    band_id = session.query(Bands).filter_by(band_name=band_name).first()
    return band_id.id

# def add_bands(id: int, band_name: str) -> None:
#     """
#     Добавление групп в БД
#
#     :param id: объект типа int
#     :param band_name: объект типа str
#     :return: None
#     """
#
#     new_band = Bands(id=id, band_name=band_name)
#
#     session.add(new_band)
#
#     session.commit()
