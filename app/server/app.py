from fastapi import FastAPI

app = FastAPI()

@app.get("/",tags=['Root'])
async def read_root():
    return {"message": "FastAPI server is running"}