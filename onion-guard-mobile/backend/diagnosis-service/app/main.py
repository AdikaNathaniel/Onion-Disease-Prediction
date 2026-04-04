import os
import io
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
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


@app.get("/history/{email}")
async def get_history(email: str):
    cursor = diagnoses_collection.find(
        {"email": email},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50)

    history = await cursor.to_list(length=50)
    return {"success": True, "history": history}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
