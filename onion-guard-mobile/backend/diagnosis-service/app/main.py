import os
import io
import json
import re
import base64
import numpy as np
import httpx
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from PIL import Image

app = FastAPI(title="OnionGuard Diagnosis Service", version="1.0.0")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "onionguard_diagnosis")
MODEL_PATH = os.getenv("MODEL_PATH", str(Path(__file__).parent.parent / "models" / "onion_model.tflite"))

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
diagnoses_collection = db["diagnoses"]

CLASS_NAMES = ["Alternaria", "Bulb_Blight", "Caterpillar", "Fusarium", "Healthy", "Virosis"]
IMG_SIZE = 224

# Lazy-load interpreter
_interpreter = None


def get_interpreter():
    global _interpreter
    if _interpreter is None:
        try:
            import tflite_runtime.interpreter as tflite
            _interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        except ImportError:
            import tensorflow as tf
            _interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        _interpreter.allocate_tensors()
    return _interpreter


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img, dtype=np.float32)
    img_array = img_array / 127.5 - 1.0  # Normalize to [-1, 1]
    return np.expand_dims(img_array, axis=0)


def predict(image_bytes: bytes) -> dict:
    interpreter = get_interpreter()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img_input = preprocess_image(image_bytes)
    interpreter.set_tensor(input_details[0]["index"], img_input)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])

    pred_idx = int(np.argmax(output[0]))
    confidence = float(output[0][pred_idx])

    return {
        "class_name": CLASS_NAMES[pred_idx],
        "confidence": round(confidence * 100, 2),
        "all_predictions": {
            name: round(float(output[0][i]) * 100, 2)
            for i, name in enumerate(CLASS_NAMES)
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "diagnosis-service"}


@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    try:
        result = predict(image_bytes)
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model file not found. Place onion_model.tflite in the models/ directory."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return {"success": True, **result}


@app.post("/predict-and-save")
async def predict_and_save(file: UploadFile = File(...), email: str = ""):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    result = predict(image_bytes)

    diagnosis_doc = {
        "email": email,
        "disease": result["class_name"],
        "confidence": result["confidence"],
        "all_predictions": result["all_predictions"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    await diagnoses_collection.insert_one(diagnosis_doc)

    return {"success": True, **result}


class SaveDiagnosisRequest(BaseModel):
    email: str
    disease: str
    confidence: float
    all_predictions: dict = {}


@app.post("/save")
async def save_diagnosis(req: SaveDiagnosisRequest):
    doc = {
        "email": req.email,
        "disease": req.disease,
        "confidence": req.confidence,
        "all_predictions": req.all_predictions,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    await diagnoses_collection.insert_one(doc)
    return {"success": True, "message": "Diagnosis saved"}


@app.get("/history/{email}")
async def get_history(email: str):
    cursor = diagnoses_collection.find(
        {"email": email},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50)

    history = await cursor.to_list(length=50)
    return {"success": True, "history": history}


# ── LLM Proxy (keys never leave the server) ─────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "anthropic/claude-3-haiku")

FRESHNESS_PROMPT = (
    'Analyze this onion image and determine its freshness level. '
    'Respond ONLY in this exact JSON format, nothing else: '
    '{"freshness": "Fresh" or "Almost Spoilt" or "Rotten", '
    '"confidence": 0-100, '
    '"description": "brief explanation of visual signs", '
    '"tips": "storage or usage recommendation"}'
)

LANG_NAMES = {
    "en": "English",
    "tw": "Twi (Akan)",
    "dg": "Dagbani",
    "ee": "Ewe",
    "ha": "Hausa",
}


def _parse_gemini_json(candidates: list) -> dict:
    if not candidates:
        raise HTTPException(status_code=502, detail="Empty Gemini response")
    parts = candidates[0].get("content", {}).get("parts", [])
    full_text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
    full_text = re.sub(r"```json\s*", "", full_text)
    full_text = re.sub(r"```\s*", "", full_text).strip()
    try:
        return json.loads(full_text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", full_text)
        if not match:
            raise HTTPException(status_code=502, detail="Could not parse Gemini response")
        return json.loads(match.group(0))


@app.post("/llm/freshness")
async def llm_freshness(file: UploadFile = File(...)):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="Gemini API key not configured")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    mime_type = "image/png" if (file.filename or "").lower().endswith(".png") else "image/jpeg"
    b64 = base64.b64encode(image_bytes).decode("ascii")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": FRESHNESS_PROMPT},
                    {"inline_data": {"mime_type": mime_type, "data": b64}},
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 1024,
            "responseMimeType": "application/json",
        },
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, json=payload)

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Gemini API failed: {resp.status_code}")

    return _parse_gemini_json(resp.json().get("candidates", []))


class TranslateRequest(BaseModel):
    text: str
    target_language: str


@app.post("/llm/translate")
async def llm_translate(req: TranslateRequest):
    if req.target_language == "en":
        return {"translated_text": req.text}
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=503, detail="OpenRouter API key not configured")

    lang_name = LANG_NAMES.get(req.target_language, "English")
    payload = {
        "model": DEFAULT_LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Translate the following text to {lang_name}. "
                    f"Return ONLY the translated text, nothing else:\n\n{req.text}"
                ),
            }
        ],
        "max_tokens": 1000,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Translation failed: {resp.status_code}")

    data = resp.json()
    try:
        translated = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError):
        raise HTTPException(status_code=502, detail="Malformed OpenRouter response")
    return {"translated_text": translated}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
