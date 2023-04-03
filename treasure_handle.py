import pytesseract
from typing import Dict
from PIL import Image
import aiogram
from aiogram.types import Message
import re


pattern = re.compile(r'\b\d+\.\d{5}\b')
api_key = ''
bot: aiogram.Bot

async def treasure_handle(message: Message) -> None:
    photo: str = message.photo[-1].file_id
    file = await bot.download_file_by_id(photo)
    result = find_coordinates(file)
    
    format_latitude = result[0].replace(".",r"\.")
    format_longitude = result[1].replace(".",r"\.")
    await message.answer(text=f'Coordinates for {format_latitude}, {format_longitude}')
    await message.answer_location(latitude=result[0], longitude=result[1])
    
    
def find_coordinates(file) -> set:
    img = Image.open(file)
    img = img.convert('L')
    text: str = pytesseract.image_to_string(img)
    result = re.findall(pattern, text)
    
    return result