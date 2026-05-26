from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db
from app.models.credit import CreditTransaction
from app.models.user import User
from app.schemas.credit import (
    CreditBalanceResponse,
    CreditTransactionResponse,
    FeatureCostItem,
    FeatureCostsResponse,
)
from app.services.credits import FEATURE_CREDIT_COSTS, FeatureType

router = APIRouter()


@router.get("/balance", response_model=CreditBalanceResponse)
async def get_balance(user: User = Depends(get_current_user)):
    return CreditBalanceResponse(credits=user.credits, membership_type=user.membership_type.value)


@router.get("/costs", response_model=FeatureCostsResponse)
async def get_feature_costs():
    costs = [
        FeatureCostItem(feature=f.value, credits=c)
        for f, c in FEATURE_CREDIT_COSTS.items()
    ]
    return FeatureCostsResponse(costs=costs)


@router.get("/transactions", response_model=list[CreditTransactionResponse])
async def list_transactions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
):
    result = await db.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == user.id)
        .order_by(CreditTransaction.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()
