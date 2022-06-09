from pydantic import BaseModel, HttpUrl


class Goals(BaseModel):
    TITLE: str
    IMAGE:bytes
    # IMAGE:  Optional[ImageSchema] = None

    class Config:
        schema_extra = {
            "example": {
                "TITLE": "Lose Weight",
                'IMAGE':"BASE64 PATH"
            }
        }
