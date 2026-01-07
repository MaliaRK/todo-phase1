# SQLModel Queries Guide

## Basic Queries

### Select Queries
```python
from sqlmodel import Session, select
from models.hero import Hero

def get_hero_by_id(session: Session, hero_id: int) -> Hero:
    statement = select(Hero).where(Hero.id == hero_id)
    hero = session.exec(statement).first()
    return hero

def get_all_heroes(session: Session) -> List[Hero]:
    statement = select(Hero)
    heroes = session.exec(statement).all()
    return heroes

def get_heroes_by_age(session: Session, min_age: int) -> List[Hero]:
    statement = select(Hero).where(Hero.age >= min_age)
    heroes = session.exec(statement).all()
    return heroes
```

### Count Queries
```python
def count_heroes(session: Session) -> int:
    statement = select(Hero).with_only_columns(func.count(Hero.id))
    count = session.exec(statement).one()
    return count

def count_heroes_by_team(session: Session, team_id: int) -> int:
    from sqlalchemy import func
    statement = select(func.count(Hero.id)).where(Hero.team_id == team_id)
    count = session.exec(statement).one()
    return count
```

## Advanced Filtering

### Multiple Conditions
```python
def get_heroes_by_criteria(
    session: Session,
    min_age: Optional[int] = None,
    team_id: Optional[int] = None,
    name_contains: Optional[str] = None
) -> List[Hero]:
    statement = select(Hero)

    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)

    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)

    if name_contains:
        statement = statement.where(Hero.name.contains(name_contains))

    heroes = session.exec(statement).all()
    return heroes
```

### Complex Conditions
```python
def get_adult_heroes_not_on_team(session: Session, team_id: int) -> List[Hero]:
    statement = select(Hero).where(
        (Hero.age >= 18) & (Hero.team_id != team_id)
    )
    heroes = session.exec(statement).all()
    return heroes

def get_heroes_with_secret_names(session: Session) -> List[Hero]:
    from sqlalchemy import and_, or_
    statement = select(Hero).where(
        and_(
            Hero.secret_name.is_not(None),
            Hero.secret_name != "",
            Hero.name != Hero.secret_name
        )
    )
    heroes = session.exec(statement).all()
    return heroes
```

## Ordering and Limiting

### Ordering Results
```python
def get_heroes_ordered_by_name(session: Session) -> List[Hero]:
    statement = select(Hero).order_by(Hero.name)
    heroes = session.exec(statement).all()
    return heroes

def get_heroes_ordered_by_age_desc(session: Session) -> List[Hero]:
    from sqlalchemy import desc
    statement = select(Hero).order_by(desc(Hero.age))
    heroes = session.exec(statement).all()
    return heroes

def get_youngest_heroes(session: Session, limit: int = 5) -> List[Hero]:
    statement = select(Hero).order_by(Hero.age).limit(limit)
    heroes = session.exec(statement).all()
    return heroes
```

### Pagination
```python
def get_heroes_paginated(
    session: Session,
    offset: int = 0,
    limit: int = 10
) -> List[Hero]:
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement).all()
    return heroes

def get_heroes_with_pagination_info(
    session: Session,
    page: int = 1,
    page_size: int = 10
) -> dict:
    offset = (page - 1) * page_size

    # Get total count
    count_statement = select(Hero).with_only_columns(func.count(Hero.id))
    total_count = session.exec(count_statement).one()

    # Get paginated results
    statement = select(Hero).offset(offset).limit(page_size)
    heroes = session.exec(statement).all()

    return {
        "heroes": heroes,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "pages": (total_count + page_size - 1) // page_size
    }
```

## Joins and Relationships

### Join Queries
```python
def get_heroes_with_teams(session: Session) -> List[tuple]:
    statement = select(Hero, Team).join(Team, isouter=True)
    results = session.exec(statement).all()
    return results

def get_heroes_from_specific_team(session: Session, team_name: str) -> List[Hero]:
    statement = select(Hero).join(Team).where(Team.name == team_name)
    heroes = session.exec(statement).all()
    return heroes

def get_teams_with_hero_count(session: Session) -> List[dict]:
    from sqlalchemy import func
    statement = (
        select(Team, func.count(Hero.id).label('hero_count'))
        .join(Hero, isouter=True)
        .group_by(Team.id)
    )
    results = session.exec(statement).all()
    return [{"team": team, "hero_count": count} for team, count in results]
```

### Subqueries
```python
def get_heroes_from_teams_with_many_heroes(session: Session, min_heroes: int = 3) -> List[Hero]:
    # Subquery to find teams with many heroes
    team_hero_counts = (
        select(Team.id)
        .join(Hero)
        .group_by(Team.id)
        .having(func.count(Hero.id) >= min_heroes)
    ).subquery()

    # Main query to get heroes from those teams
    statement = select(Hero).where(Hero.team_id.in_(select(team_hero_counts.c.id)))
    heroes = session.exec(statement).all()
    return heroes
```

## Update Operations

### Single Record Updates
```python
def update_hero_age(session: Session, hero_id: int, new_age: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero with id {hero_id} not found")

    hero.age = new_age
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

def update_hero_secret_name(session: Session, hero_id: int, new_secret_name: str) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero with id {hero_id} not found")

    hero.secret_name = new_secret_name
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

### Bulk Updates
```python
def bulk_update_heroes_age(session: Session, team_id: int, age_increment: int):
    from sqlalchemy import update

    statement = (
        update(Hero)
        .where(Hero.team_id == team_id)
        .values(age=Hero.age + age_increment)
    )
    result = session.exec(statement)
    session.commit()
    return result.rowcount
```

## Delete Operations

### Single Record Deletion
```python
def delete_hero_by_id(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if not hero:
        return False

    session.delete(hero)
    session.commit()
    return True

def safe_delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if not hero:
        return False

    # Check for dependencies if needed
    if hero.team:
        # Handle team relationship if necessary
        pass

    session.delete(hero)
    session.commit()
    return True
```

### Bulk Deletion
```python
def delete_heroes_by_team(session: Session, team_id: int) -> int:
    from sqlalchemy import delete

    statement = delete(Hero).where(Hero.team_id == team_id)
    result = session.exec(statement)
    session.commit()
    return result.rowcount

def delete_heroes_by_age_range(session: Session, min_age: int, max_age: int) -> int:
    from sqlalchemy import delete

    statement = delete(Hero).where((Hero.age >= min_age) & (Hero.age <= max_age))
    result = session.exec(statement)
    session.commit()
    return result.rowcount
```

## Transactions

### Simple Transactions
```python
from sqlmodel import Session
from contextlib import contextmanager

@contextmanager
def get_session_with_transaction(engine):
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

def transfer_hero_to_team(
    session: Session,
    hero_id: int,
    new_team_id: int
) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero with id {hero_id} not found")

    hero.team_id = new_team_id
    session.add(hero)
    return hero

# Usage
def safely_transfer_hero(engine, hero_id: int, new_team_id: int):
    with get_session_with_transaction(engine) as session:
        return transfer_hero_to_team(session, hero_id, new_team_id)
```

### Complex Transactions
```python
def complex_hero_operation(
    session: Session,
    hero_id: int,
    new_team_id: int,
    new_age: int
) -> dict:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise ValueError(f"Hero with id {hero_id} not found")

    old_team_id = hero.team_id

    # Update hero
    hero.team_id = new_team_id
    hero.age = new_age
    session.add(hero)

    # Update team statistics if needed
    if old_team_id:
        old_team = session.get(Team, old_team_id)
        if old_team:
            # Decrement old team's hero count (if tracking)
            pass

    new_team = session.get(Team, new_team_id)
    if new_team:
        # Increment new team's hero count (if tracking)
        pass

    return {
        "hero": hero,
        "old_team_id": old_team_id,
        "new_team_id": new_team_id
    }
```

## Query Optimization

### Using Indexes Effectively
```python
def get_hero_by_name_indexed(session: Session, name: str) -> Hero:
    # Assumes Hero.name has an index
    statement = select(Hero).where(Hero.name == name)
    hero = session.exec(statement).first()
    return hero

def get_heroes_by_multiple_criteria_indexed(
    session: Session,
    name_prefix: str,
    min_age: int
) -> List[Hero]:
    # Assumes indexes on name and age
    statement = select(Hero).where(
        Hero.name.startswith(name_prefix),
        Hero.age >= min_age
    )
    heroes = session.exec(statement).all()
    return heroes
```

### Avoiding N+1 Queries
```python
def get_heroes_with_teams_optimized(session: Session) -> List[dict]:
    from sqlalchemy.orm import selectinload

    statement = select(Hero).options(selectinload(Hero.team))
    heroes = session.exec(statement).all()

    return [
        {
            "hero": hero,
            "team": hero.team
        }
        for hero in heroes
    ]
```

## Error Handling

### Handling Common Query Errors
```python
from sqlalchemy.exc import IntegrityError, NoResultFound

def create_hero_safe(session: Session, hero_data: dict) -> Hero:
    try:
        hero = Hero(**hero_data)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    except IntegrityError:
        session.rollback()
        raise ValueError("Hero already exists or violates unique constraint")
    except Exception as e:
        session.rollback()
        raise e

def get_hero_or_none(session: Session, hero_id: int) -> Optional[Hero]:
    try:
        statement = select(Hero).where(Hero.id == hero_id)
        hero = session.exec(statement).one()
        return hero
    except NoResultFound:
        return None
    except Exception:
        raise
```