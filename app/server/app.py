from fastapi import FastAPI
from app.server.routes.user import router as userRouter
from app.server.routes.wallet import router as walletRouter

app=FastAPI()

app.include_router(userRouter,tags=['user'],prefix="/user")
app.include_router(walletRouter,tags=['wallet'],prefix='/wallet')



@app.get("/",tags=['Root'])
async def read_root():
    return {"message": "FastAPI server is running"}