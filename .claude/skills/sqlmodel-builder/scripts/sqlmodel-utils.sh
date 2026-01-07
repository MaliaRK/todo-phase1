#!/bin/bash
# SQLModel utility script

# Function to create a new SQLModel project structure
create_project() {
  local project_name=$1
  local project_dir=$project_name

  if [ -z "$project_name" ]; then
    echo "Usage: $0 create-project <project-name>"
    exit 1
  fi

  mkdir -p "$project_dir"/{models,crud,routers,api}

  # Create requirements.txt
  cat > "$project_dir/requirements.txt" << 'EOF'
sqlmodel==0.0.16
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
python-dotenv==1.0.0
EOF

  # Create database setup
  cat > "$project_dir/database.py" << 'EOF'
from sqlmodel import create_engine, Session
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
EOF

  # Create main app
  cat > "$project_dir/main.py" << 'EOF'
from fastapi import FastAPI
from database import engine
from sqlmodel import SQLModel

app = FastAPI(title="SQLModel API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "SQLModel API"}
EOF

  # Create basic model
  cat > "$project_dir/models/hero.py" << 'EOF'
from sqlmodel import SQLModel, Field
from typing import Optional

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, ge=0)

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
EOF

  echo "Created SQLModel project: $project_dir"
  echo "To run the project:"
  echo "  cd $project_dir"
  echo "  pip install -r requirements.txt"
  echo "  uvicorn main:app --reload"
}

# Function to create a new SQLModel model
create_model() {
  local model_name=$1
  local model_file="models/${model_name}.py"

  if [ -z "$model_name" ]; then
    echo "Usage: $0 create-model <model-name>"
    exit 1
  fi

  mkdir -p models

  # Convert to proper case for class names
  model_class=$(echo "$model_name" | sed 's/.*/\u&/')

  cat > "$model_file" << EOF
from sqlmodel import SQLModel, Field
from typing import Optional

class ${model_class}Base(SQLModel):
    # Add your fields here
    # name: str = Field(index=True)
    # description: Optional[str] = None
    pass

class ${model_class}(${model_class}Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ${model_class}Create(${model_class}Base):
    pass

class ${model_class}Update(SQLModel):
    # Add optional fields for updates
    # name: Optional[str] = None
    # description: Optional[str] = None
    pass

class ${model_class}Public(${model_class}Base):
    id: int
EOF

  echo "Created SQLModel model: $model_file"
}

# Function to create CRUD operations for a model
create_crud() {
  local model_name=$1
  local crud_file="crud/${model_name}.py"

  if [ -z "$model_name" ]; then
    echo "Usage: $0 create-crud <model-name>"
    exit 1
  fi

  mkdir -p crud

  # Convert to proper case for class names
  model_class=$(echo "$model_name" | sed 's/.*/\u&/')

  cat > "$crud_file" << EOF
from sqlmodel import Session, select
from models.${model_name} import ${model_class}, ${model_class}Create, ${model_class}Update
from typing import List, Optional

def get_${model_name}(session: Session, ${model_name}_id: int) -> Optional[${model_class}]:
    return session.get(${model_class}, ${model_name}_id)

def get_${model_name}s(session: Session, offset: int = 0, limit: int = 100) -> List[${model_class}]:
    statement = select(${model_class}).offset(offset).limit(limit)
    return session.exec(statement).all()

def create_${model_name}(session: Session, ${model_name}_create: ${model_class}Create) -> ${model_class}:
    db_${model_name} = ${model_class}.model_validate(${model_name}_create)
    session.add(db_${model_name})
    session.commit()
    session.refresh(db_${model_name})
    return db_${model_name}

def update_${model_name}(
    session: Session,
    ${model_name}_id: int,
    ${model_name}_update: ${model_class}Update
) -> Optional[${model_class}]:
    db_${model_name} = session.get(${model_class}, ${model_name}_id)
    if db_${model_name}:
        update_data = ${model_name}_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_${model_name}, key, value)
        session.add(db_${model_name})
        session.commit()
        session.refresh(db_${model_name})
    return db_${model_name}

def delete_${model_name}(session: Session, ${model_name}_id: int) -> bool:
    db_${model_name} = session.get(${model_class}, ${model_name}_id)
    if db_${model_name}:
        session.delete(db_${model_name})
        session.commit()
        return True
    return False
EOF

  echo "Created CRUD operations: $crud_file"
}

# Main script
case $1 in
  "create-project")
    if [ -z "$2" ]; then
      echo "Usage: $0 create-project <project-name>"
      exit 1
    fi
    create_project "$2"
    ;;
  "create-model")
    if [ -z "$2" ]; then
      echo "Usage: $0 create-model <model-name>"
      exit 1
    fi
    create_model "$2"
    ;;
  "create-crud")
    if [ -z "$2" ]; then
      echo "Usage: $0 create-crud <model-name>"
      exit 1
    fi
    create_crud "$2"
    ;;
  *)
    echo "Usage: $0 {create-project|create-model|create-crud} [name]"
    echo "  create-project: Create a new SQLModel project structure"
    echo "  create-model: Create a new SQLModel model"
    echo "  create-crud: Create CRUD operations for a model"
    exit 1
    ;;
esac