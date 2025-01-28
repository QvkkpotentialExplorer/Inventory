from sqlalchemy import Column, Integer, Text, TIMESTAMP, text, String, ForeignKey, CheckConstraint
from data.data import Base


class InventoryRepair(Base):
    __tablename__ = 'inventory_repairs'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    request_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(String, nullable=False)
    description = Column(Text)

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in_progress', 'completed')", name="check_repair_status"),
    )