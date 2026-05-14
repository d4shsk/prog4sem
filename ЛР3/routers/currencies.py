from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
import models
import schemas
from cbr_service import fetch_and_update_currencies

router = APIRouter(prefix="/currencies", tags=["Currencies"])

@router.get("/", response_model=list[schemas.CurrencyOut])
async def read_currencies(db: AsyncSession = Depends(get_db)):
    stmt = select(models.Currency)
    result = await db.execute(stmt)
    return list(result.scalars().all())

@router.post("/update")
async def update_currencies(db: AsyncSession = Depends(get_db)):
    try:
        await fetch_and_update_currencies(db)
        return {"detail": "Валюты успешно обновлены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось обновить валюты: {str(e)}")

@router.get("/{currency_code}/rate")
async def get_currency_rate(currency_code: str, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Currency).where(models.Currency.code == currency_code)
    result = await db.execute(stmt)
    currency = result.scalar_one_or_none()
    
    if not currency:
        raise HTTPException(status_code=404, detail="Валюта не найдена")
        
    return {"code": currency.code, "rate": currency.rate}
