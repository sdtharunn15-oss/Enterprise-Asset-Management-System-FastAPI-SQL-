from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    asset_name = Column(String(100), nullable=False)

    category = Column(String(100), nullable=False)

    status = Column(String(50), nullable=False)

    # ✅ NEW FIELD (Soft Delete)
    is_deleted = Column(Boolean, default=False)