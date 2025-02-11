from fastapi import APIRouter, status
from service.schemas import PostImageRequest, ResponseImageRequest
import httpx
import json
import os

router = APIRouter(
    prefix="/llava",
    tags=["llava-API"]
)


async def llava_call(ollama_url: str, data: dict):
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", ollama_url, json=data) as response:
            full_response = []
            combined_message = ''
            async for line in response.aiter_lines():
                if line.strip():  # Avoid empty lines
                    try:
                        json_line = json.loads(line)
                        full_response.append(json_line)
                        response_text = json_line.get("response", "")
                        combined_message += response_text  # Concatenate responses
                    except json.JSONDecodeError:
                        continue  # Ignore malformed lines
            return full_response, combined_message.strip()  # Return both the list and the combined string


async def save_response_to_json(data, response, combined_message, filename="responses.json"):
    # Create the response object in the desired format
    response_data = {
        "data": data,
        "response": response,
        "combined_message": combined_message
    }

    # Check if the file exists
    if os.path.exists(filename):
        # If file exists, append the new response
        with open(filename, "r+") as file:
            existing_data = json.load(file)
            existing_data.append(response_data)  # Append the new data
            file.seek(0)  # Move the cursor to the beginning of the file to overwrite
            json.dump(existing_data, file, indent=4)
    else:
        # If file doesn't exist, create a new one and write the response
        with open(filename, "w") as file:
            json.dump([response_data], file, indent=4)  # Write as a list of dictionaries

        
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseImageRequest)
async def main_call(request: PostImageRequest):
    
    ollama_url = 'http://192.168.20.111:11434/api/generate'

    data = {
        "model": request.model,
        "prompt": request.prompt,
        "images": request.images
    }

    response, combined_message = await llava_call(ollama_url, data)
    await save_response_to_json(data, response, combined_message)

    return {"response": combined_message}
