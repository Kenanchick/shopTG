from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user, get_category, get_item_cards, get_card_by_id, add_to_cart_db
import app.keyboards as kb

user = Router()

@user.callback_query(F.data == 'start')
@user.message(CommandStart())
async def cmd_start(event: Message | CallbackQuery):
    await set_user(event.from_user.id)
    if isinstance(event, Message):
        await event.answer('Добро пожаловать в бот!', reply_markup=kb.menu)
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.delete()
        await event.message.answer('Добро пожаловать в бот!', reply_markup=kb.menu)        
        
        
@user.callback_query(F.data == 'catalog')
async def get_catalog(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(photo ='AgACAgIAAxkBAANhZ8Wr0nq5Kv77rTDJR0lCB22gH6AAAr7uMRs3LylKbW_v39wCnewBAAMCAAN4AAM2BA', caption = 'Выберите категорию товара!', 
    reply_markup= await kb.categories())
    

@user.callback_query(F.data.startswith('cat_'))
async def get_itemcard(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_info = await get_category(category_id)
    await callback.message.delete()
    await callback.message.answer_photo(photo=category_info.image, caption=f'{category_info.title}\n\n{category_info.description}', reply_markup= await kb.items_cards(category_id))
    

@user.callback_query(F.data.startswith('card_'))
async def get_card(callback: CallbackQuery):
    card = await get_card_by_id(callback.data.split('_')[1])
    await callback.message.delete()
    await callback.message.answer(f'{card.title}\n\nОписание: {card.description}\n\nЦена:  {card.price} рублей\n\nИнструкция: {card.instruction}', reply_markup= await kb.add_to_cart(card))
    
@user.callback_query(F.data.startswith('add_to_cart_'))
async def add_tocart(callback: CallbackQuery):
    card_id = callback.data.split('_')[2]
    user_id = callback.from_user.id
    
    await add_to_cart_db(card_id, user_id)
    await callback.message.answer("✅ Товар добавлен в корзину!")

@user.message(F.photo)
async def get_photo(message: Message):
    category_info
    await message.answer(text = message.photo[-1].file_id)
    

    
