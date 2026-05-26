"""Credits system — feature costs and balance management."""

from enum import Enum

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.credit import CreditTransaction, CreditTransactionType
from app.models.user import User

SIGNUP_BONUS = 100


class FeatureType(str, Enum):
    POSITION_MATCH = "position_match"
    PROFESSOR_ANALYSIS = "professor_analysis"
    EMAIL_GENERATION = "email_generation"
    SOP_GENERATION = "sop_generation"
    AI_POLISH = "ai_polish"
    DEEP_RESEARCH = "deep_research"


FEATURE_CREDIT_COSTS: dict[FeatureType, int] = {
    FeatureType.POSITION_MATCH: 5,
    FeatureType.PROFESSOR_ANALYSIS: 10,
    FeatureType.EMAIL_GENERATION: 15,
    FeatureType.SOP_GENERATION: 30,
    FeatureType.AI_POLISH: 8,
    FeatureType.DEEP_RESEARCH: 50,
}


async def grant_credits(
    db: AsyncSession,
    user: User,
    amount: int,
    reason: str,
    tx_type: CreditTransactionType = CreditTransactionType.GRANT,
) -> User:
    user.credits += amount
    db.add(
        CreditTransaction(
            user_id=user.id,
            type=tx_type,
            amount=amount,
            reason=reason,
        )
    )
    await db.flush()
    return user


async def spend_credits(
    db: AsyncSession,
    user: User,
    feature: FeatureType,
    reason: str | None = None,
) -> int:
    cost = FEATURE_CREDIT_COSTS[feature]
    if user.credits < cost:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient credits. Need {cost}, have {user.credits}",
        )
    user.credits -= cost
    db.add(
        CreditTransaction(
            user_id=user.id,
            type=CreditTransactionType.SPEND,
            amount=-cost,
            reason=reason or feature.value,
        )
    )
    await db.flush()
    return cost


def get_feature_cost(feature: FeatureType) -> int:
    return FEATURE_CREDIT_COSTS[feature]
