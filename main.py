from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Base, SessionLocal
from models import User, Group
from schemas import UserCreate, GroupCreate, UserResponse, GroupResponse, UserDetail, UserUpdate


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, number=user.number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.group_ids:
        for group_id in user.group_ids:
            group = db.query(Group).filter(Group.id == group_id).first()
            if group:
                db_user.groups.append(group)
            else:
                raise HTTPException(status_code=404, detail=f"Group with id {group_id} not found")
        db.commit()
        db.refresh(db_user)

    return db_user


@app.put("/users/{user_id}", response_model=UserDetail)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.number = user.number
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


@app.get("/groups/", response_model=List[GroupResponse])
def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups


@app.get("/groups/{group_id}", response_model=GroupResponse)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@app.post("/groups/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    if group.user_ids:
        for user_id in group.user_ids:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db_group.users.append(user)
            else:
                raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        db.commit()
        db.refresh(db_group)

    return db_group


@app.delete("/groups/{group_id}", response_model=GroupResponse)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(db_group)
    db.commit()
    return db_group
    

@app.post("/groups/{group_id}/add_user/{user_id}", response_model=GroupResponse)
def add_user_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user not in db_group.users:
        db_group.users.append(db_user)
        db.commit()
        db.refresh(db_group)
    
    return db_group

@app.delete("/groups/{group_id}/remove_user/{user_id}", response_model=GroupResponse)
def remove_user_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user in db_group.users:
        db_group.users.remove(db_user)
        db.commit()
        db.refresh(db_group)
    
    return db_group
