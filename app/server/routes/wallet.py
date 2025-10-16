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

@router.get('/id/{id}',response_description='waller data retrive by wallet id')
async def get_wallet(id:str):
    wallet=await retrive_wallet(id)
    if wallet:
        return responseModel(wallet, "wallets data retrieved successfully")
    return ErrorResponseModel(wallet, "Empty list returned")

@router.get('/user/{user_id}',response_description='waller data retrive by user id')
async def get_wallet(user_id:str):
    wallet=await retrieve_wallet_by_user(user_id)
    if wallet:
        return responseModel(wallet, "wallets data retrieved successfully")
    return ErrorResponseModel(wallet, "Empty list returned")

