from service.config import settings
from fastapi import HTTPException, status
from service.schemas import OllamaCallModel
import httpx
import json


class OllamaCall:
    def __init__(self):
        self.api_url =  settings.ollama_api_url
        self.data: OllamaCallModel = None
        self.response: str = None

    
    def request_data(self, model:str = None, prompt:str = None, images: list[str] = None):
        self.data = OllamaCallModel(
            model = model,
            prompt = prompt,
            images = images
        )

    async def call(self):
        if not self.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing parameters required to make a request to ollama"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                try:
                    async with client.stream("POST", self.api_url, json=self.data.__dict__, timeout=30.0) as response:
                        if response.status_code != 200:
                            raise HTTPException(
                                status_code=status.HTTP_BAD_GATEWAY,
                                detail=f"Ollama API returned status code {response.status_code}"
                            )
                        
                        combined_message = ''
                        async for line in response.aiter_lines():
                            if line.strip():
                                try:
                                    json_line = json.loads(line)
                                    response_text = json_line.get("response", "")
                                    combined_message += response_text
                                except json.JSONDecodeError:
                                    print(f"Failed to parse JSON: {line}")
                                    continue
                        self.response = combined_message
                except httpx.RequestError as exc:
                    raise HTTPException(
                        status_code=status.HTTP_SERVICE_UNAVAILABLE,
                        detail=f"Error communicating with Ollama API: {str(exc)}"
                    )
                except httpx.TimeoutException:
                    raise HTTPException(
                        status_code=status.HTTP_GATEWAY_TIMEOUT,
                        detail="Request to Ollama API timed out"
                    )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

        
