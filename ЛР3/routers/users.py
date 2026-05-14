from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database import get_db
import models
import schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        db_user.subscribed_currencies = []
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Имя пользователя или email уже зарегистрированы")

@router.get("/", response_model=list[schemas.UserOut])
async def read_users(db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(selectinload(models.User.subscriptions).selectinload(models.Subscription.currency))
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    for user in users:
        user.subscribed_currencies = [sub.currency for sub in user.subscriptions]
    return list(users)

@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(selectinload(models.User.subscriptions).selectinload(models.Subscription.currency)).where(models.User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    user.subscribed_currencies = [sub.currency for sub in user.subscriptions]
    return user

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).options(selectinload(models.User.subscriptions).selectinload(models.Subscription.currency)).where(models.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
        
    try:
        await db.commit()
        await db.refresh(db_user)
        db_user.subscribed_currencies = [sub.currency for sub in db_user.subscriptions]
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Имя пользователя или email уже существуют")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).where(models.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
        
    await db.delete(db_user)
    await db.commit()
    return None
