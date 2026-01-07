# crud/{{model_name}}.py
from sqlmodel import Session, select
from models.{{model_name}} import {{model_name.capitalize()}}, {{model_name.capitalize()}}Create, {{model_name.capitalize()}}Update
from typing import List, Optional

def get_{{model_name}}(session: Session, {{model_name}}_id: int) -> Optional[{{model_name.capitalize()}}]:
    """
    Get a {{model_name}} by ID.
    """
    return session.get({{model_name.capitalize()}}, {{model_name}}_id)

def get_{{model_names}}(session: Session, skip: int = 0, limit: int = 100) -> List[{{model_name.capitalize()}}]:
    """
    Get a list of {{model_names}} with pagination.
    """
    statement = select({{model_name.capitalize()}}).offset(skip).limit(limit)
    return session.exec(statement).all()

def create_{{model_name}}(session: Session, {{model_name}}_create: {{model_name.capitalize()}}Create) -> {{model_name.capitalize()}}:
    """
    Create a new {{model_name}}.
    """
    db_{{model_name}} = {{model_name.capitalize()}}.model_validate({{model_name}}_create)
    session.add(db_{{model_name}})
    session.commit()
    session.refresh(db_{{model_name}})
    return db_{{model_name}}

def update_{{model_name}}(
    session: Session,
    {{model_name}}_id: int,
    {{model_name}}_update: {{model_name.capitalize()}}Update
) -> Optional[{{model_name.capitalize()}}]:
    """
    Update an existing {{model_name}}.
    """
    db_{{model_name}} = session.get({{model_name.capitalize()}}, {{model_name}}_id)
    if db_{{model_name}}:
        update_data = {{model_name}}_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_{{model_name}}, key, value)
        session.add(db_{{model_name}})
        session.commit()
        session.refresh(db_{{model_name}})
    return db_{{model_name}}

def delete_{{model_name}}(session: Session, {{model_name}}_id: int) -> bool:
    """
    Delete a {{model_name}} by ID.
    """
    db_{{model_name}} = session.get({{model_name.capitalize()}}, {{model_name}}_id)
    if db_{{model_name}}:
        session.delete(db_{{model_name}})
        session.commit()
        return True
    return False