from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey, BLOB, Float
from sqlalchemy.dialects.postgresql import BYTEA

from crud.databases import DeclarativeBase


class Style(DeclarativeBase):
    """
    Класс Style для создания объектов типа style и добавления их в БД
    """

    __tablename__ = 'styles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    style = Column('style', String, unique=True)
    description = Column('description', String)
    image = Column('image', BYTEA)

    def __repr__(self):
        return f"id={self.id}, style={self.style}, description={self.description}, image={self.image}"


class Bands(DeclarativeBase):
    """
    Класс Band для создания объектов типа bands и добавления их в БД
    """

    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    band_name = Column('band_name', String, unique=True)

    def __repr__(self):
        return f"id={self.id}, band_name={self.band_name}"


class BandsStyles(DeclarativeBase):
    """
    Класс BandsStyles для создания объектов типа style_id, band_id и добавления их в БД
    """

    __tablename__ = 'band_style'
    __table_args__ = (
        PrimaryKeyConstraint('style_id', 'band_id'),
    )

    style_id = Column(Integer, ForeignKey('styles.id'))
    band_id = Column(Integer, ForeignKey('bands.id'))

    def __repr__(self):
        return f"style_id={self.style_id}, band_id={self.band_id}"


class Songs(DeclarativeBase):
    """
    Класс Song для создания объектов типа song и добавления их в БД
    """

    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    style_id = Column(Integer, ForeignKey('styles.id'))
    band_id = Column(Integer, ForeignKey('bands.id'))

    song_name = Column('song_name', String, unique=True)
    song_text = Column('song_text', String)
    data_ogg = Column('data_ogg', BYTEA)

    def __repr__(self):
        # return f"style_id={self.style_id}, band_id={self.band_id}, song_name={self.song_name}, song_text={self.song_text}, data_ogg={self.data_ogg}"
        return f"{self.__class__.__name__}(style_id={self.style_id}, band_id={self.band_id}, song_name={self.song_name}, song_text={self.song_text}, data_ogg={self.data_ogg})"


class Score(DeclarativeBase):
    """
    Класс Player для создания объектов типа player и добавления их в БД
    """
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True, autoincrement=True)
    songs_id = Column(Integer, ForeignKey('songs.id'))
    name = Column('name', String)
    time = Column(Float)



    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.songs_id}, name={self.name}, time={self.time})"


