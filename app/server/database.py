import os
from dotenv import load_dotenv
import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime

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

def transaction_helper(transaction)-> dict:
    return {
        "id": str(transaction["_id"]),
        'from_user':transaction['from_user'],
        'to_user':transaction['to_user'],
        'amount':transaction['amount'],
        'type':transaction['type'],  
        'status':transaction['status'],
        'timestamp': transaction['timestamp']
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
    wallet_data = {
        "user_id": str(new_user["_id"]),
        "balance": 0.0,
        "currency": "USD"
    }
    await add_wallet(wallet_data) 
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
    
# transactions crud collection

async def create_transaction(from_user_id: str, to_user_id: str, amount: float, t_type="transaction") -> dict:
    
    # Retrieve wallets automatically
    from_wallet = await retrieve_wallet_by_user(from_user_id)
    to_wallet = await retrieve_wallet_by_user(to_user_id)
    if not from_wallet or not to_wallet:
        return {"error": "Invalid user or wallet"}

    # Check sufficient balance
    if from_wallet["balance"] < amount:
        return {"error": "Insufficient balance"}

    # Update balances atomically
    await wallet_collection.update_one({"_id": ObjectId(from_wallet["id"])}, {"$inc": {"balance": -amount}})
    await wallet_collection.update_one({"_id": ObjectId(to_wallet["id"])}, {"$inc": {"balance": amount}})

    # Create transaction record
    transaction_data = {
        "from_user": from_user_id,
        "to_user": to_user_id,
        "amount": amount,
        "type": t_type,
        "status": "success",
        "timestamp": datetime.utcnow()  # <-- NEW: auto timestamp
    }
    transaction = await transaction_collection.insert_one(transaction_data)
    new_transaction = await transaction_collection.find_one({"_id": transaction.inserted_id})
    return transaction_helper(new_transaction)

async def retrive_transactions(user_id: str):
    transactions = []
    async for transaction in transaction_collection.find({
        "$or": [{"from_user": user_id}, {"to_user": user_id}]
    }):
        transactions.append(transaction_helper(transaction))
    return transactions
        
    
async def retrive_transaction_by_id(transaction_id:str):
    transaction= await transaction_collection.find_one({'_id': ObjectId(transaction_id)})
    if transaction:
        return transaction_helper(transaction)

async def delete_transaction(transaction_id:str):
    transaction= await transaction_collection.find_one({'_id': ObjectId(transaction_id)})
    if transaction:
        await transaction_collection.delete_one({'_id': ObjectId(transaction_id)})
        return True
