import pytesseract
from typing import Dict
from PIL import Image
import aiogram
from aiogram.types import Message
import re
import asyncio

pattern = re.compile(r'\b\d+\.\d{5}\b')
bot: aiogram.Bot

async def treasure_handle(message: Message) -> None:
    photo: str = message.photo[-1].file_id
    file = await bot.download_file_by_id(photo)
    result = find_coordinates(file)
    
    format_latitude = result[0].replace(".",r"\.")
    format_longitude = result[1].replace(".",r"\.")
    text_replay = await message.answer(text=f'Coordinates for {format_latitude}, {format_longitude}')
    map_replay = await message.answer_location(latitude=result[0], longitude=result[1])
    
    await asyncio.sleep(60)

    await message.delete()
    await map_replay.delete()
    await text_replay.delete()


async def treasure_rejecte(message: Message) -> None:
    await message.answer("Send picture, bro!")


def find_coordinates(file) -> set:
    img = Image.open(file)
    img = img.convert('L')
    text: str = pytesseract.image_to_string(img)
    result = re.findall(pattern, text)
    
    return result