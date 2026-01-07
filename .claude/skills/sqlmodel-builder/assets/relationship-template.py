# models/{{model_name}}_with_relationship.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class {{model_name.capitalize()}}(SQLModel, table=True):
    __tablename__ = "{{table_name}}"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    # Add other fields as needed

    # Add foreign key field if this model references another
    # {{related_model}}_id: Optional[int] = Field(default=None, foreign_key="{{related_table}}.id")

    # Define relationships
    # {{related_model_plural}}: List["{{related_model.capitalize()}}"] = Relationship(back_populates="{{reverse_relationship}}")

class {{related_model.capitalize()}}(SQLModel, table=True):
    __tablename__ = "{{related_table}}"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    # Add other fields as needed

    # Add foreign key field if this model is referenced by another
    # {{model_name}}_id: Optional[int] = Field(default=None, foreign_key="{{table_name}}.id")

    # Define relationships
    # {{model_name_plural}}: List["{{model_name.capitalize()}}"] = Relationship(back_populates="{{reverse_relationship}}")