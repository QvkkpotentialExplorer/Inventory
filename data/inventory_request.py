from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text, CheckConstraint
from data.data import Base


class InventoryRequest(Base):
    __tablename__ = 'inventory_requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventory.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    request_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    status = Column(String, nullable=False)
    count = Column(Integer,nullable=False)
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="check_request_status"),
    )
