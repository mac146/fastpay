from fastapi import FastAPI
from app.server.routes.user import router as userRouter

app=FastAPI()

app.include_router(userRouter,tags=['user'],prefix="/user")



@app.get("/",tags=['Root'])
async def read_root():
    return {"message": "FastAPI server is running"}