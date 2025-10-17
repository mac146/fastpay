from typing import Optional,Literal
from pydantic import Field,BaseModel
from datetime import datetime

class TransactionSchema(BaseModel):
    from_user:Optional[str]
    to_user:str=Field(...)
    amount:float=Field(...,gt=0.0)
    type:Literal['add-funds', 'transfer']  
    status:Literal['success', 'failed']
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Transaction timestamp")

class TransactionStatusUpdateModel(BaseModel):
    status: Literal['success', 'failed']
