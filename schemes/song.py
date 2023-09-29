from pydantic import BaseModel


class Song(BaseModel):
    band_name: str
    song_name: str
    song_text: str
    data_ogg: bytes