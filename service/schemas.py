from pydantic import BaseModel

class PostImageRequest(BaseModel):
    model: str
    prompt: str
    images: list[str]


class ResponseImageRequest(BaseModel):
    response: str