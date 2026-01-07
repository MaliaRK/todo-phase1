# FastAPI Routing and APIRouters Guide

## Application Structure with APIRouters

Use APIRouter to organize your endpoints in a modular way:

```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.user import User, UserCreate
from dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    # Implementation here
    pass

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    # Implementation here
    pass

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    # Implementation here
    pass
```

```python
# main.py
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
```

## Path Parameters and Validation

FastAPI automatically validates path parameters:

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: str = None
):
    return {"item_id": item_id, "q": q}
```

## Query Parameters and Validation

Define query parameters with validation:

```python
from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        description="Query string for items"
    ),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, le=100, description="Maximum number of items to return")
):
    results = {"items": [{"item_id": 1}, {"item_id": 2}]}
    if q:
        results.update({"q": q})
    return results
```

## Request Body and Pydantic Models

Define request bodies using Pydantic models:

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## Multiple Path Operations

Handle different HTTP methods for the same path:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": "Item deleted"}
```

## Advanced Request Body Features

### Multiple Body Parameters
```python
from typing import Optional

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: Optional[str] = None
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

### Body Fields
```python
from pydantic import Field

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None
```

## Form Data and File Uploads

Handle form data and file uploads:

```python
from fastapi import File, Form, UploadFile

@app.post("/files/")
async def create_file(
    file: bytes = File(..., description="File as bytes"),
    fileb: UploadFile = File(..., description="Uploaded file"),
    token: str = Form(..., description="Form token")
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb": {
            "filename": fileb.filename,
            "content_type": fileb.content_type
        }
    }
```

## Response Models

Define response models for validation:

```python
from fastapi import FastAPI

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True

class UserInDB(User):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: User):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! But not really")
    return user_in_db

@app.post("/user/", response_model=User)
async def create_user(user_in: User):
    user_saved = fake_save_user(user_in)
    return user_saved
```