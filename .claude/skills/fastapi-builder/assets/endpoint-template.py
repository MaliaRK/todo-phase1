# routers/{{endpoint_name}}.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.{{endpoint_name}} import {{endpoint_name.capitalize()}}Response, {{endpoint_name.capitalize()}}Create, {{endpoint_name.capitalize()}}Update
from dependencies import get_current_user, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/{{endpoint_name}}",
    tags=["{{endpoint_name}}"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[{{endpoint_name.capitalize()}}Response])
async def read_{{endpoint_name}}(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve {{endpoint_name}}.
    """
    # Implementation here
    pass

@router.post("/", response_model={{endpoint_name.capitalize()}}Response, status_code=status.HTTP_201_CREATED)
async def create_{{endpoint_name}}(
    {{endpoint_name}}: {{endpoint_name.capitalize()}}Create,
    db: Session = Depends(get_db)
):
    """
    Create a new {{endpoint_name}}.
    """
    # Implementation here
    pass

@router.get("/{id}", response_model={{endpoint_name.capitalize()}}Response)
async def read_{{endpoint_name}}_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific {{endpoint_name}} by ID.
    """
    # Implementation here
    pass

@router.put("/{id}", response_model={{endpoint_name.capitalize()}}Response)
async def update_{{endpoint_name}}(
    id: int,
    {{endpoint_name}}_update: {{endpoint_name.capitalize()}}Update,
    db: Session = Depends(get_db)
):
    """
    Update an existing {{endpoint_name}}.
    """
    # Implementation here
    pass

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{{endpoint_name}}(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a {{endpoint_name}}.
    """
    # Implementation here
    pass