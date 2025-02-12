from pydantic import BaseModel

class PostImageRequest(BaseModel):
    file: str
    model: str
    prompt: str
    images: list[str]


class ResponseImageRequest(BaseModel):
    response: str