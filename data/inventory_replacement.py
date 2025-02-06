from sqlalchemy import Column

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text, CheckConstraint
from data.data import Base

class InventoryReplacement(Base):
    __tablename__ = 'inventory_replacement'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    usage_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(String, nullable=False)
    reason_description = Column(String)
    photo = Column(String,nullable=False)
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="check_request_status"),
    )
