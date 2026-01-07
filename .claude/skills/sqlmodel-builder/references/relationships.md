# SQLModel Relationships Guide

## One-to-Many Relationships

### Basic One-to-Many
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # One team has many heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

    # Many heroes belong to one team
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Creating Related Objects
```python
from sqlmodel import Session, create_engine, select

# Create team
team = Team(name="Avengers", headquarters="Stark Tower")

# Create heroes with the team
hero1 = Hero(name="Iron Man", secret_name="Tony Stark", team=team)
hero2 = Hero(name="Captain America", secret_name="Steve Rogers", team=team)

# Add to session
session.add(team)  # This also adds the heroes due to the relationship
session.commit()
```

## Many-to-Many Relationships

### Using an Association Table
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Association table for many-to-many relationship
class TeamHeroLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # Many-to-many relationship through the association table
    heroes: List["Hero"] = Relationship(
        back_populates="teams",
        link_model=TeamHeroLink
    )

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

    # Many-to-many relationship through the association table
    teams: List["Team"] = Relationship(
        back_populates="heroes",
        link_model=TeamHeroLink
    )
```

## One-to-One Relationships

### Basic One-to-One
```python
class Identity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    real_name: str
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", unique=True)

    # One-to-one relationship
    hero: Optional["Hero"] = Relationship(back_populates="identity")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None)

    # One-to-one relationship
    identity_id: Optional[int] = Field(default=None, foreign_key="identity.id", unique=True)
    identity: Optional["Identity"] = Relationship(back_populates="hero")
```

## Self-Referential Relationships

### Hierarchical Data
```python
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Self-referential relationships
    parent: Optional["Category"] = Relationship(back_populates="subcategories")
    subcategories: List["Category"] = Relationship(back_populates="parent")
```

## Relationship Loading Strategies

### Eager Loading
```python
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

# Eager load heroes when fetching teams
def get_teams_with_heroes(session: Session):
    statement = select(Team).options(selectinload(Team.heroes))
    teams = session.exec(statement).all()
    return teams

# Eager load team when fetching heroes
def get_heroes_with_teams(session: Session):
    statement = select(Hero).options(selectinload(Hero.team))
    heroes = session.exec(statement).all()
    return heroes
```

### Lazy Loading
```python
# Lazy loading - relationships are loaded when accessed
def get_hero_with_lazy_team(session: Session, hero_id: int):
    hero = session.get(Hero, hero_id)
    # Team is loaded only when hero.team is accessed
    team_name = hero.team.name if hero.team else "No team"
    return hero, team_name
```

## Relationship Operations

### Adding Related Objects
```python
def add_hero_to_team(session: Session, hero_id: int, team_id: int):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)

    # Add hero to team
    team.heroes.append(hero)
    session.add(team)
    session.commit()
```

### Removing Related Objects
```python
def remove_hero_from_team(session: Session, hero_id: int):
    hero = session.get(Hero, hero_id)

    # Remove hero from team (assuming one-to-many)
    if hero.team:
        hero.team.heroes.remove(hero)
        session.add(hero.team)

    session.delete(hero)
    session.commit()
```

### Many-to-Many Operations
```python
def assign_hero_to_team(session: Session, hero_id: int, team_id: int):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)

    # Add to many-to-many relationship
    hero.teams.append(team)
    session.add(hero)
    session.commit()

def remove_hero_from_team(session: Session, hero_id: int, team_id: int):
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)

    # Remove from many-to-many relationship
    hero.teams.remove(team)
    session.add(hero)
    session.commit()
```

## Relationship Validation

### Custom Validation in Relationships
```python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, ge=0)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="heroes")

    @field_validator('team_id')
    def validate_team_exists(cls, v, values):
        # This is a simplified example - actual validation would require database access
        if v is not None:
            # In a real scenario, you'd check if the team exists in the database
            pass
        return v
```

## Relationship Querying

### Querying with Relationships
```python
def get_heroes_by_team_name(session: Session, team_name: str):
    statement = select(Hero).join(Team).where(Team.name == team_name)
    heroes = session.exec(statement).all()
    return heroes

def get_teams_with_hero_count(session: Session):
    from sqlalchemy import func
    statement = (
        select(Team, func.count(Hero.id).label('hero_count'))
        .join(Hero, isouter=True)
        .group_by(Team.id)
    )
    results = session.exec(statement).all()
    return results

def get_heroes_without_teams(session: Session):
    statement = select(Hero).where(Hero.team_id.is_(None))
    heroes = session.exec(statement).all()
    return heroes
```

## Cascade Operations

### Cascade Options
```python
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    # Cascade options can be configured through SQLAlchemy options
    heroes: List["Hero"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"  # Delete heroes when team is deleted
        }
    )
```

## Relationship Best Practices

### 1. Always Define Back-References
```python
# Good - bidirectional relationship
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### 2. Use Proper Typing
```python
from typing import Optional, List

class Team(SQLModel, table=True):
    # Use Optional for single relationships
    hero: Optional["Hero"] = Relationship(...)
    # Use List for multiple relationships
    heroes: List["Hero"] = Relationship(...)
```

### 3. Consider Performance Implications
```python
# For large datasets, consider lazy loading
# and only eager load when necessary
def get_team_summary(session: Session, team_id: int):
    # Just get team info without loading all heroes
    team = session.get(Team, team_id)
    return {"id": team.id, "name": team.name, "headquarters": team.headquarters}
```