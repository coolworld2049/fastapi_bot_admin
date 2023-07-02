import base64
from typing import Optional

from pydantic import BaseModel


# data:video/mp4;base64,...


class ReactFile(BaseModel):
    src: Optional[str]
    title: Optional[str]

    @property
    def content_type(self):
        try:
            return self.src.split(",")[0].split(":")[1].split(";")[0]
        except:
            return None

    @property
    def encoding(self):
        try:
            return self.src.split(",")[0].split(";")[1]
        except:
            return None

    @property
    def file_data(self):
        try:
            string = self.src.split(",")[1]
            return base64.b64decode(string)
        except:
            return None

    class Config:
        orm_mode = True
