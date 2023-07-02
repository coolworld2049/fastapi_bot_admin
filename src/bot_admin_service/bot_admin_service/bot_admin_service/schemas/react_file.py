import base64
from typing import Optional

from pydantic import BaseModel


# data:video/mp4;base64,...


class ReactFile(BaseModel):
    src: Optional[str]
    title: Optional[str]

    @property
    def content_type(self):
        return self.src.split(",")[0].split(":")[1].split(";")[0]

    @property
    def encoding(self):
        return self.src.split(",")[0].split(";")[1]

    @property
    def file_data(self):
        string = self.src.split(",")[1]
        return base64.b64decode(string)

    @property
    def filename(self):
        return self.title

    class Config:
        orm_mode = True
