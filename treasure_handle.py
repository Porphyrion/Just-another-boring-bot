import pytesseract
from typing import Dict
from PIL import Image
import aiogram
import googlemaps
from aiogram.types import Message
import re


pattern = re.compile(r'\b\d+\.\d{5}\b')
api_key = ''
bot: aiogram.Bot

async def treasure_handle(message: Message) -> None:
    print('recievd')
    photo: str = message.photo[-1].file_id
    file = await bot.download_file_by_id(photo)
    result: str = process_picture(file)

    await message.answer(chat_id=message.chat.id, text=result)


def process_picture(file) -> str:
    coordinates = find_coordinates(file)
    
    return get_link_to_coordinates(coordinates)


def find_coordinates(file) -> set:
    img = Image.open(file)
    img = img.convert('L')
    text: str = pytesseract.image_to_string(img)
    result = re.findall(pattern, text)
    print(result)
    
    return result



def get_link_to_coordinates(coordinates):
    gmaps = googlemaps.Client(key=api_key) 
    results = gmaps.reverse_geocode(coordinates)

    if results:
        address = results[0]['formatted_address']
        place_id = results[0]['place_id']
        map_link = f'https://www.google.com/maps/place/?q=place_id:{place_id}'

        return(f'The place at {coordinates} is {address}\nMap link: {map_link}')
    else:
        return('No results found.')