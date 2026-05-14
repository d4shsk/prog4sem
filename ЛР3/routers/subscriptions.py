from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import get_db
import models
import schemas

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_subscription(sub: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Currency).where(models.Currency.code == sub.currency_code)
    result = await db.execute(stmt)
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Валюта не найдена")

    stmt_user = select(models.User).where(models.User.id == sub.user_id)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db_sub = models.Subscription(user_id=sub.user_id, currency_id=currency.id)
    db.add(db_sub)
    try:
        await db.commit()
        return {"detail": "Подписка успешно создана"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Подписка уже существует")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(sub: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Currency).where(models.Currency.code == sub.currency_code)
    result = await db.execute(stmt)
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Валюта не найдена")

    stmt_sub = select(models.Subscription).where(
        models.Subscription.user_id == sub.user_id,
        models.Subscription.currency_id == currency.id
    )
    result_sub = await db.execute(stmt_sub)
    db_sub = result_sub.scalar_one_or_none()

    if not db_sub:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    await db.delete(db_sub)
    await db.commit()
    return None
