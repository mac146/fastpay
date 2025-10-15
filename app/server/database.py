import os
from dotenv import load_dotenv
import motor.motor_asyncio
from bson.objectid import ObjectId
load_dotenv()
MONGO_DETAILS=os.getenv('MONGO_DETAILS')
client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database=client.fastpay
user_collection=database.get_collection('users')
wallet_collection=database.get_collection('wallet')
transaction_collection=database.get_collection('transaction')

def user_helper(user)->dict:
    return {
        "id":str(user["_id"]),
        "fullname":user["fullname"],
        "email":user["email"],
    }

def wallet_helper(wallet) -> dict:
    return {
        "id": str(wallet["_id"]),
        "user_id": str(wallet["user_id"]),
        "balance": wallet["balance"],
        "currency": wallet["currency"]
    }

def transfer_helper(transfer)-> dict:
    return {
        'from_user':transfer['from_user'],
        'to_user':transfer['to_user'],
        'amount':transfer['amount'],
        'type':transfer['type'],  
        'status':transfer['status'],
        'timestamp': transfer['timestamp']
  }

#users crud collection

async def retrive_users():
    users=[]
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

async def retrive_user(id:str)->dict:
    user=await user_collection.find_one({"_id":ObjectId(id)})
    if user:
      return user_helper(user)

async def add_user(user_data:dict)->dict:
    user=await user_collection.insert_one(user_data)
    new_user=await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def update_user(id:str,data:dict):
    if len(data)<1:
        return False
    user=await user_collection.find_one({"_id":ObjectId(id)})
    if user:
        updated_user=await user_collection.update_one({"_id":ObjectId(id)},{"$set":data})
        if updated_user.modified_count > 0:
            return True
        return False
    
async def delete_user(id:str):
    user=await user_collection.find_one({"_id":ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id":ObjectId(id)})
        return True
    
#wallet crud collection

async def add_wallet(wallet_data:dict)->dict:
    wallet_data.setdefault("balance", 0.0)
    wallet=await wallet_collection.insert_one(wallet_data)
    new_wallet=await wallet_collection.find_one({"_id": wallet.inserted_id})
    return wallet_helper(new_wallet)

async def retrive_wallet(id:str)->dict:
    wallet=await wallet_collection.find_one({'_id':ObjectId(id)})
    if wallet:
        return wallet_helper(wallet)
    
async def retrieve_wallet_by_user(user_id: str) -> dict:
    wallet = await wallet_collection.find_one({'user_id': user_id})
    if wallet:
        return wallet_helper(wallet)
    
async def update_wallet(user_id:str,data:dict):
    if len(data)<1:
        return False
    
    if "balance" in data and data["balance"] < 0:
        return False
    wallet=await wallet_collection.find_one({'user_id': user_id})
    if wallet:
        updated_wallet=await wallet_collection.update_one({"user_id":user_id},{"$set":data})
        if updated_wallet.modified_count > 0:
            return True
        return False
    
async def delete_wallet(id:str):
    wallet=await wallet_collection.find_one({"_id":ObjectId(id)})
    if wallet:
        await wallet_collection.delete_one({"_id":ObjectId(id)})
        return True