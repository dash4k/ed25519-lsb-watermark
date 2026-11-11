from fastapi import FastAPI, Request
from nacl.signing import VerifyKey
from src.config import VERIFY_KEY_PATH
from src.utils import verify_embedded_from_bytes

with open(VERIFY_KEY_PATH, "rb") as f:
    verify_key = VerifyKey(f.read())

app = FastAPI()

@app.post("/verify")
async def process(request: Request):
    data = await request.body()
    result = verify_embedded_from_bytes(data, verify_key)
    return {"result": result}