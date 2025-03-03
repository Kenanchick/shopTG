from app.database.models import async_session
from app.database.models import User, Category, Item_card, Item, Cart
from sqlalchemy import select, update, delete, desc, insert


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    
async def get_category(category_id):
    async with async_session() as session:
        return await session.scalar(select(Category).where(Category.id == category_id))
    
    
async def get_item_cards(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item_card).where(Item_card.category_id == category_id))
    

async def get_card_by_id(card_id):
        async with async_session() as session:
            return await session.scalar(select(Item_card).where(Item_card.id == card_id)) 
        
async def add_to_cart_db(card_id, tg_id):
        async with async_session() as session:
            print('Wwwwwwwwwwww')
            cart_item = await session.scalar(select(Cart).where(Cart.user_id == tg_id, Cart.item_card_id == card_id)) 
            
        if cart_item:
            stmt = (
                update(Cart)
                .where(Cart.user_id == tg_id, Cart.item_card_id == card_id)
                .values(count=cart_item.count+ 1)
            )
        else:
            stmt = insert(Cart).values(user_id=tg_id, item_card_id=card_id, count=1)

        await session.execute(stmt)
        await session.commit()
