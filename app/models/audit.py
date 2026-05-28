from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Audit(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String)  # ASSIGNED / RETURNED

    user_id = Column(Integer)

    asset_id = Column(Integer)

    timestamp = Column(DateTime, default=datetime.utcnow)