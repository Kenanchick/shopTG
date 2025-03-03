from sqlalchemy import ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(515))
    image: Mapped[str] = mapped_column(String(256))
        
class Item_card(Base):
    __tablename__ = 'item_cards'
    
    id: Mapped[int] = mapped_column(primary_key=True)    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(String(120))
    instruction: Mapped[str] = mapped_column(String(128))
    
class Item(Base):
    __tablename__ = 'items'
    
    id: Mapped[int] = mapped_column(primary_key=True)  
    item_card_id: Mapped[int] = mapped_column(ForeignKey('item_cards.id'))  
    data: Mapped[str] = mapped_column(String(128))
    bought: Mapped[bool] = mapped_column(default=False)
        
class Cart(Base):
    __tablename__ = 'carts'
    
    id: Mapped[int] = mapped_column(primary_key=True)  
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))    
    item_card_id: Mapped[int] = mapped_column(ForeignKey('item_cards.id'))
    count: Mapped[int]
    


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
