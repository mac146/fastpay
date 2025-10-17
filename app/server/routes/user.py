from fastapi import APIRouter,Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_user,
    delete_user,
    retrive_users,
    retrive_user,
    update_user
)

from app.server.models.user_model import(
    UserSchema,
    UserModel
)

from app.server.models.response_model import(
    responseModel,
    ErrorResponseModel
)

router=APIRouter()

@router.post('/',response_description="user registered in db")
async def add_user_data(user:UserSchema=Body(...)):
    user=jsonable_encoder(user)
    new_user=await add_user(user)
    return responseModel(new_user,'user added succesfully')

@router.get('/',response_description='users data retrieved')
async def get_users():
    users=await retrive_users()
    if users:
        return responseModel(users, "users data retrieved successfully")
    return ErrorResponseModel(users,404, "Empty list returned")

@router.get('/{id}',response_description='user data retrieved')
async def get_user(id:str):
    user=await retrive_user(id)
    if user:
        return responseModel(user, "users data retrieved successfully")
    return ErrorResponseModel(user,404, "Empty list returned")

@router.put('/{id}',response_description='updating user data')
async def update_user_data(id:str,req:UserModel):
    req={k:v for k, v in req.dict().items() if v is not None}
    updated_user=await update_user(id,req)
    if updated_user:
        return responseModel(
            "user with ID: {} data update is successful".format(id),
            "user data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )

@router.delete('/{id}',response_description='deleting user data')
async def delete_user_data(id:str):
    deleted_user=await delete_user(id)
    if deleted_user:
        return responseModel(
            "user with ID: {} data deleted is successful".format(id),
            "users data deleted successfully",
        )
    
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )