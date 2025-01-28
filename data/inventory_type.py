from sqlalchemy import Column, Integer, String, Text, orm
from data.data import Base
import sqlalchemy


class InventoryType(Base):
    __tablename__ = 'inventory_type'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False,unique=True)
    description = Column(Text)
    photo = Column(String,nullable=True,default='')
