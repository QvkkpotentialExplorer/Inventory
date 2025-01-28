from sqlalchemy import Column, String, Integer, Text, CheckConstraint, ForeignKey, Date
from data.data import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    inventory_type_id = Column(Integer,ForeignKey('inventory_type.id',onupdate="NO ACTION", ondelete="NO ACTION"))
    status = Column(String, nullable=False, default='new')
    description = Column(Text)
    assignment_date = Column(Date, nullable=True)
    user_id = Column(String,ForeignKey('users.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)
    username = Column(String,  ForeignKey('users.username', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('new', 'used', 'broken', 'in_use')", name="check_inventory_condition"),
    )