from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text, CheckConstraint
from data.data import Base


class InventoryReport(Base):
    __tablename__ = 'inventory_reports'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False)
    usage_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    condition_before = Column(String, nullable=False)
    condition_after = Column(String, nullable=False)
    description = Column(String,nullable=False)
    photo = Column(String,nullable=False)
    __table_args__ = (
        CheckConstraint("condition_before IN ('new', 'used', 'broken')", name="check_condition_before"),
        CheckConstraint("condition_after IN ('new', 'used', 'broken')", name="check_condition_after"),
    )