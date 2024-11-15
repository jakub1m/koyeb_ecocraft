from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncio
import json
import os

from prompts.expert_chat import ExpertChat
from prompts.recycling_guidance import RecyclingGuide
from prompts.upcycling_ideas import UpcyclingIdeas
from prompts.waste_detection import WasteDetection
from prompts.recycling_guidance2 import RecyclingGuide2

from utils.image_fetcher import fetch_image
from utils.logging_config import log_execution, logger
from fastapi.middleware.cors import CORSMiddleware

api_key = os.getenv("GEMINI_API_KEY", "")

expert_chat = ExpertChat(api_key)
recycling_guide = RecyclingGuide(api_key)
upcycling_ideas = UpcyclingIdeas(api_key)
waste_detection = WasteDetection(api_key)
recycling_guide2 = RecyclingGuide2(api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)

bins = {"Plastik i metal":"https://i.ibb.co/vZ1qkNv/PLASTIK.png","Papier":"https://i.ibb.co/YcfRc0r/PAPIER.png","Szkło":"https://i.ibb.co/X2tMqzT/SZKLO.png","Odpady organiczne":"https://i.ibb.co/HVS5WpD/BIO.png","Odpady zmieszane":"https://i.ibb.co/SX38LP9/ZMIESZANE.png","Odpady wielkogabarytowe":"https://i.postimg.cc/tg5j4NDv/GABARYTY2.png","brak":"https://i.ibb.co/7JD4yZn/nie-rozpoznano.png"}

class MessageModel(BaseModel):
    Message: str


class PhotoModel(BaseModel):
    Photo_URL: str


class UpcyclingTextModel(BaseModel):
    Message: list[dict]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@log_execution
@app.post('/expert')
async def expert_endpoint(data: MessageModel):
    response = await expert_chat.generate_response(data.Message)
    return {"response": response}


@log_execution
@app.post('/detect')
async def waste_detect(data: PhotoModel):
    image = await fetch_image(data.Photo_URL)
    response = await waste_detection.generate_response(image)
    return {"response": response}


@log_execution
@app.post('/recycling_text')
async def recycling_text_endpoint(data: MessageModel):
    response = await recycling_guide.generate_response(data.Message)
    return {"response": response}


@log_execution
@app.post('/recycling_photo')
async def recycling_photo_endpoint(data: PhotoModel):
    image = await fetch_image(data.Photo_URL)
    response = await recycling_guide2.generate_response(image)
    cleaned = response.split("```json\n")[1].split("```")[0].replace("'", '"')
    gemini_response = json.loads(cleaned)
    for item in gemini_response:
        item['bin'] = bins.get(item['bin'], bins["brak"])
    grouped_by_bin = {}

    for item in gemini_response:
        bin_url = item["bin"]
        item_info = {
            "item": item["item"],
            "explanation": item["explanation"]
        }
        
        if bin_url not in grouped_by_bin:
            grouped_by_bin[bin_url] = []
        
        grouped_by_bin[bin_url].append(item_info)
    return {"response": gemini_response, "bins": grouped_by_bin}



@log_execution
@app.post('/recycling_photo_2')
async def recycling_photo_endpoint_2(data: PhotoModel):
    photo = await fetch_image(data.Photo_URL)
    described_photo = await waste_detection.generate_response(photo)
    response = await recycling_guide.generate_response()
    
    cleaned = response.split("```json\n")[1].split("```")[0]
    gemini_response = json.loads(cleaned)
    for item in gemini_response:
        item['bin'] = bins.get(item['bin'])
    grouped_by_bin = {}

    for item in data:
        bin_url = item["bin"]
        item_info = {
            "item": item["item"],
            "explanation": item["explanation"]
        }
        
        if bin_url not in grouped_by_bin:
            grouped_by_bin[bin_url] = []
        
        grouped_by_bin[bin_url].append(item_info)
    return {"response": gemini_response, "bins": grouped_by_bin}


@log_execution
@app.post('/upcycling_text')
async def upcycling_endpoint(data: UpcyclingTextModel):
    json_string = json.dumps(data.Message, ensure_ascii=False, indent=4)
    response = await upcycling_ideas.generate_response(json_string)
    cleaned = response.split("```json\n")[1].split("```")[0].replace("'", '"')
    return {"response": json.loads(cleaned)}


@log_execution
@app.post('/upcycling_photo')
async def upcycling_photo_endpoint(data: PhotoModel):
    image = await fetch_image(data.Photo_URL)
    items = await recycling_guide2.generate_response(image)
    cleaned = items.split("```json\n")[1].split("```")[0].replace("'", '"')
    data = [{"item": entry["item"], "details": entry["details"]} for entry in json.loads(cleaned)]
    json_string = json.dumps(data, ensure_ascii=False, indent=4)
    response = await upcycling_ideas.generate_response(json_string)
    cleaned = response.split("```json\n")[1].split("```")[0].replace("'", '"')
    return {"response": json.loads(cleaned)}


# To run the FastAPI server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=2024)
