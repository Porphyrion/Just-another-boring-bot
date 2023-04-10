import pytesseract
from PIL import Image
from aiogram import types, Bot
import re
import asyncio
import logging

pattern = re.compile(r'\b\d+\.\d{5}\b')
bot: Bot

logging.basicConfig(level=logging.INFO)

async def treasure_handle(message: types.Message) -> None:
    logging.info(f'treasure_handle() for uset {message.from_user.id}')
    
    photo: str = message.photo[-1].file_id
    file = await bot.download_file_by_id(photo)
    result = find_coordinates(file)
    
    if len(result) == 2:
        await succese_answer(message, result, file)
    else:
        await sorry_answer(message, file)
    

async def treasure_rejecte(message: types.Message) -> None:
    logging.info(f'treasure_rejecte() for uset {message.from_user.id}')
    await message.answer("Send picture, bro!")


def find_coordinates(file) -> set:
    img = Image.open(file)
    
    coord = parse_image(img)
    if len(coord) != 2:
        coord = parse_image(img, True)
    
    return coord


def parse_image(img, invert=False) ->set:
    if invert:
        img = img.convert('L')
    
    text: str = pytesseract.image_to_string(img)
    return re.findall(pattern, text)


def format_coordinates(coord) ->str:
    return  coord[0].replace(".",r"\.") + coord[1].replace(".",r"\.")


async def sorry_answer(message: types.Message, file):
    
    # logging.info(f'File saved in {file.name}')
    
    await message.answer(text='Sorry, can`t find coordinates')
    await eat_breadcrumbs(message)


async def succese_answer(message: types.Message, coord, file):
    del file
      
    text_format = format_coordinates(coord)
    text_replay = await message.answer(text=f'Coordinates for {text_format}')
    map_replay = await message.answer_location(latitude=coord[0], longitude=coord[1])
    
    await eat_breadcrumbs(text_format, text_replay, map_replay)


async def eat_breadcrumbs(message, replay_message=None, replay_map=None):
    await asyncio.sleep(60)

    try:
        await message.delete()
        await replay_map.delete()
        await replay_message.delete()
    except TypeError:
        print("Caught TypeError: Cannot call my_method on None object")
        
    
    