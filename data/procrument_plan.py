from sqlalchemy import Column, Integer, Text, TIMESTAMP, text, String, ForeignKey, DECIMAL
from data.data import Base


class ProcurementPlan(Base):
    __tablename__ = 'procurement_plans'

    id = Column(Integer, primary_key=True)
    inventory_type_id = Column(Integer, ForeignKey('inventory_type.id', onupdate="NO ACTION", ondelete="NO ACTION"),
                          nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL, nullable=False)
    supplier = Column(String, nullable=False)
    planned_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
