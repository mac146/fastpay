from typing import Optional
from pydantic import BaseModel,Field

class WalletSchema(BaseModel):
    user_id: str = Field(...)
    balance:float=Field(...,ge=0.0)
    currency:str=Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "670cd112d812f3c9b4b7b8a2",
                "balance": 0.0,
                "currency": "INR"
            }
        }

class WalletUpdateModel(BaseModel):
    balance:Optional[float]
    currency:Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "balance": 500.0,
                "currency": "INR"
            }
        }

