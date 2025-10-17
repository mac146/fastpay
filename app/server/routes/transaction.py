from fastapi import APIRouter,Body
from fastapi.encoders import jsonable_encoder

from app.server.models.response_model import (
    responseModel,
    ErrorResponseModel
)

from app.server.models.transfer_model import (
    TransactionSchema,
    TransactionStatusUpdateModel
)

from app.server.database import (
    create_transaction,
    delete_transaction,
    retrive_transactions,
    retrive_transaction_by_id
)

router=APIRouter()

@router.post('/', response_description="Transaction registered")
async def add_transfer_data(transfer: TransactionSchema = Body(...)):
    transfer_data = jsonable_encoder(transfer)
    
    new_transfer = await create_transaction(
        from_user_id=transfer_data['from_user'],
        to_user_id=transfer_data['to_user'],
        amount=transfer_data['amount'],
        t_type=transfer_data.get('type', 'transaction')
    )

    if "error" in new_transfer:
        return ErrorResponseModel(new_transfer["error"], 400, "Transaction failed")

    return responseModel(new_transfer, 'Transaction added successfully')


@router.get('/user/{user_id}',response_description='transfer data retrieved through user id')
async def get_transfers(user_id:str):
    transfers=await retrive_transactions(user_id)
    if transfers:
        return responseModel(transfers, "transfers data retrieved successfully")
    return ErrorResponseModel(transfers, "Empty list returned")

@router.get('/id/{transaction_id}',response_description='transfer data retrieved through transaction_id')
async def get_transfer(transaction_id:str):
    transfers=await retrive_transaction_by_id(transaction_id)
    if transfers:
        return responseModel(transfers, "transfers data retrieved successfully")
    return ErrorResponseModel(transfers, "Empty list returned")

@router.delete('/{transaction_id}',response_description='deleting transactions detail')
async def delete_transfer(transaction_id:str):
    deleted_transaction=await delete_transaction(transaction_id)
    if deleted_transaction:
        return responseModel(
            "transaction with ID: {} data deleted is successful".format(transaction_id),
            "transaction data deleted successfully",
        )
    
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )