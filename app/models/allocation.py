from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from app.database import Base


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    asset_id = Column(Integer, ForeignKey("assets.id"))

    assigned_at = Column(DateTime, default=datetime.utcnow)

    returned_at = Column(DateTime, nullable=True)