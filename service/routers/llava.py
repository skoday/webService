from fastapi import APIRouter, status
from service.schemas import PostImageRequest, ResponseImageRequest
from service.ollama_call import OllamaCall
from contextlib import asynccontextmanager
from service.save_csv import AsyncCSVLogger
from service.config import settings


CSV_LOGGER = None
CSV_FILENAME = settings.csv_filename

@asynccontextmanager
async def lifespan(app: APIRouter):
    global CSV_LOGGER
    CSV_LOGGER = AsyncCSVLogger(CSV_FILENAME)
    yield


app = APIRouter(
    prefix="/llava",
    tags=["llava-API"],
    lifespan=lifespan
)

        
@app.post("", status_code=status.HTTP_201_CREATED, response_model=ResponseImageRequest)
async def main_call(request: PostImageRequest):
    
    ollama = OllamaCall()
    ollama.request_data(
        model=request.model,
        prompt=request.prompt,
        images=request.images
    )
    await ollama.call()
    response = ollama.response.strip()
    await CSV_LOGGER.save_info(request.file, request.model, request.prompt, response)
    
    return {"response": response}
