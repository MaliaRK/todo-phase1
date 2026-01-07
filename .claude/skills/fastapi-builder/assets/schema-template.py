# schemas/{{schema_name}}.py
from pydantic import BaseModel
from typing import Optional

class {{schema_name}}Base(BaseModel):
    # Define your fields here
    # name: str
    # description: Optional[str] = None
    pass

class {{schema_name}}Create({{schema_name}}Base):
    # Add required fields for creation
    pass

class {{schema_name}}Update({{schema_name}}Base):
    # Add fields that can be updated
    pass

class {{schema_name}}({{schema_name}}Base):
    id: int
    # Add other fields as needed

    class Config:
        from_attributes = True