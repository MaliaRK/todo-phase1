# models/{{model_name}}.py
from sqlmodel import SQLModel, Field
from typing import Optional

class {{model_name.capitalize()}}Base(SQLModel):
    # Define your base fields here
    # name: str = Field(index=True)
    # description: Optional[str] = None
    pass

class {{model_name.capitalize()}}({{model_name.capitalize()}}Base, table=True):
    __tablename__ = "{{table_name}}"

    id: Optional[int] = Field(default=None, primary_key=True)
    # Add your fields here with proper typing and constraints
    # name: str = Field(index=True, min_length=1, max_length=100)
    # description: Optional[str] = Field(default=None, max_length=500)
    # age: Optional[int] = Field(default=None, ge=0, le=150)

class {{model_name.capitalize()}}Create({{model_name.capitalize()}}Base):
    # Fields required for creation
    pass

class {{model_name.capitalize()}}Update(SQLModel):
    # Optional fields for updates
    # name: Optional[str] = None
    # description: Optional[str] = None
    pass

class {{model_name.capitalize()}}Public({{model_name.capitalize()}}Base):
    id: int
    # Add fields to return in public responses