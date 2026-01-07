# models/{{model_name}}.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class {{model_name}}(Base):
    __tablename__ = "{{table_name}}"

    id = Column(Integer, primary_key=True, index=True)
    # Add your columns here
    # name = Column(String, index=True)
    # description = Column(String, index=True)
    # is_active = Column(Boolean, default=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add relationships if needed
    # items = relationship("Item", back_populates="owner")