import os
from dotenv import load_dotenv
import motor.motor_asyncio
from bson.objectid import ObjectId
load_dotenv()
MONGO_DETAILS=os.getenv('MONGO_DETAILS')
client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database=client.fastpay
user_collection=database.get_collection('users_collection')

