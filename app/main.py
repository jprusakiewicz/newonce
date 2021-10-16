import uvicorn
from fastapi import FastAPI

from app.first_module import first_module

app = FastAPI()


@app.get("/")
async def get():
    return {"status": "ok"}

app.include_router(first_module.router, prefix='/first_module')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=1)
