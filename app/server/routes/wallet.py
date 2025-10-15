from fastapi import APIRouter,Body
from fastapi.encoders import jsonable_encoder

from app.server.models.response_model import (
    responseModel,
    ErrorResponseModel
)

from app.server.models.wallet_model import (
    WalletSchema,
    WalletUpdateModel
)

from app.server.database import (
    add_wallet,
    delete_wallet,
    update_wallet,
    retrive_wallet,
    retrieve_wallet_by_user
)

router=APIRouter()

@router.post('/',response_description="wallet data added into the database")
async def add_wallet_data(wallet:WalletSchema=Body(...)):
    wallet=jsonable_encoder(wallet)
    new_wallet=await add_wallet(wallet)
    return responseModel(new_wallet,'wallet added succesfully')