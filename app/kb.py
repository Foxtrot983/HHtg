from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from .reqs import get_resumes, get_vacs
from .config import AUTH_URL, CLIENT_ID

menu = [
    [
    InlineKeyboardButton(text="Получить апи ключ", url=AUTH_URL.replace('{client_id}', CLIENT_ID))
    ]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)


async def resumes_kb(token:str):
    data = await get_resumes(access_token=token)
    resume_pick = [
        [InlineKeyboardButton(text=f"{x.get('name')}", callback_data=f"resume:{x.get('id')}")] for x in data
    ]
    resume_pick_kb = InlineKeyboardMarkup(inline_keyboard=resume_pick, parse_mode='HTML', disable_web_page_preview=True)
    return resume_pick_kb


async def vacs_kb(resume_id:str, access_token:str):
    data = await get_vacs(resume_id=resume_id, access_token=access_token)
    
    vacs_kb = [
        [InlineKeyboardButton(text=f"{x.get('name')}", url=x.get('url'))] for x in data
    ]
    vacs_kb.append([InlineKeyboardButton(text=f"Вернуться к списку резюме", callback_data=f"resume_choice")])
    vacs_kb = InlineKeyboardMarkup(inline_keyboard=vacs_kb, parse_mode='HTML', disable_web_page_preview=True)
    return vacs_kb