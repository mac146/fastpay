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
    return ErrorResponseModel(wallet,404, "Empty list returned")

@router.get('/user/{user_id}',response_description='waller data retrive by user id')
async def get_wallet_user(user_id:str):
    wallet=await retrieve_wallet_by_user(user_id)
    if wallet:
        return responseModel(wallet, "wallets data retrieved successfully")
    return ErrorResponseModel(wallet, 404,"Empty list returned")

@router.put('/{user_id}',response_description='updating wallet data')
async def update_wallet_data(user_id:str,req:WalletUpdateModel):
    req={k:v for k, v in req.dict().items() if v is not None}
    updated_wallet=await update_wallet(user_id,req)
    if updated_wallet:
        return responseModel(
            "wallet with ID: {} data update is successful".format(user_id),
            "wallet data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the wallet data.",
    )

@router.delete('/{id}',response_description='deleting wallet data')
async def delete_wallet_data(id:str):
    deleted_wallet=await delete_wallet(id)
    if deleted_wallet:
        return responseModel(
            "wallet with ID: {} data deleted is successful".format(id),
            "wallet data deleted successfully",
        )
    
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )