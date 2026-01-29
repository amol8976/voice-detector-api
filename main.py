import base64
import hashlib
import time
from fastapi import Request
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI(title="Voice AI Detector")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# ⚠️ TEMP STORE (Replace with DB later)
API_KEYS = {
    "aca5afe0613152182835af9ad4e0df25494274061750cde29e2b9d8e8f70fb22": {
        "owner": "local-test",
        "rate_limit": "10/minute"
    }
}

class DetectRequest(BaseModel):
    audio_base64: str
    language: str

def validate_api_key(x_api_key: str = Header(...)):
    key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
    if key_hash not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return API_KEYS[key_hash]

@app.post("/api/v1/voice/detect")
@limiter.limit("10/minute")
def detect_voice(
    request: Request,
    req: DetectRequest,
    api_key=Depends(validate_api_key)
):

    try:
        audio_bytes = base64.b64decode(req.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64")

    # 🔴 MOCK ML (replace later)
    confidence = 0.92

    return {
        "classification": "AI_GENERATED",
        "confidence": confidence,
        "language": req.language,
        "model_version": "v1.0",
        "timestamp": int(time.time())
    }

