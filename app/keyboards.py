from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_categories, get_item_cards



menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
    [InlineKeyboardButton(text='Корзина', callback_data='cart')],
    [InlineKeyboardButton(text='Контакты', callback_data='contacts')]
])

async def categories():
    all_category = await get_categories()
    keyboard = InlineKeyboardBuilder()
    
    for cat in all_category:
        keyboard.add(InlineKeyboardButton(text=cat.title, callback_data=f'cat_{cat.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='start'))
    

    return keyboard.adjust(2).as_markup()

async def items_cards(category_id):
    all_cards = await get_item_cards(category_id)
    keyboard = InlineKeyboardBuilder()
    
    for card in all_cards:
        keyboard.add(InlineKeyboardButton(text=card.title, callback_data=f'card_{card.id}'))
    keyboard.add(InlineKeyboardButton(text='В каталог', callback_data='catalog'))
    return keyboard.adjust(1).as_markup()

async def add_to_cart(card):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart_{card.id}')],
        [InlineKeyboardButton(text='Купить сразу', callback_data=f'buy_now_{card.id}')],
        [InlineKeyboardButton(text='Назад', callback_data=f'cat_{card.category_id}')]
    ])
    
