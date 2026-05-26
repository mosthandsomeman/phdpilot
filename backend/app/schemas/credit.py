from datetime import datetime

from pydantic import BaseModel


class CreditTransactionResponse(BaseModel):
    id: int
    type: str
    amount: int
    reason: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CreditBalanceResponse(BaseModel):
    credits: int
    membership_type: str


class FeatureCostItem(BaseModel):
    feature: str
    credits: int


class FeatureCostsResponse(BaseModel):
    costs: list[FeatureCostItem]
