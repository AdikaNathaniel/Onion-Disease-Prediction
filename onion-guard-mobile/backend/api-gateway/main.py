import os
import httpx
from fastapi import FastAPI, Request, Response, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io

app = FastAPI(title="OnionGuard API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
DIAGNOSIS_URL = os.getenv("DIAGNOSIS_SERVICE_URL", "http://localhost:8002")
TREATMENT_URL = os.getenv("TREATMENT_SERVICE_URL", "http://localhost:8003")
ANALYTICS_URL = os.getenv("ANALYTICS_SERVICE_URL", "http://localhost:8004")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


# ── Auth Service Proxy ───────────────────────────────────────────────────────

@app.post("/api/v1/auth/register")
async def register(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/register", json=body, timeout=15)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.post("/api/v1/auth/login")
async def login(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/login", json=body, timeout=15)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.get("/api/v1/auth/profile/{email}")
async def get_profile(email: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{AUTH_URL}/profile/{email}", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.post("/api/v1/auth/change-password")
async def change_password(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/change-password", json=body, timeout=15)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.post("/api/v1/auth/forgot-password/{email}")
async def forgot_password(email: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_URL}/forgot-password/{email}", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


# ── Diagnosis Service Proxy ──────────────────────────────────────────────────

@app.post("/api/v1/diagnosis/predict")
async def predict(file: UploadFile = File(...)):
    file_bytes = await file.read()
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{DIAGNOSIS_URL}/predict",
            files={"file": (file.filename, file_bytes, file.content_type)},
            timeout=30,
        )
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.get("/api/v1/diagnosis/history/{email}")
async def diagnosis_history(email: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{DIAGNOSIS_URL}/history/{email}", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


# ── Treatment Service Proxy ──────────────────────────────────────────────────

@app.get("/api/v1/treatment/{disease_name}")
async def get_treatment(disease_name: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TREATMENT_URL}/treatment/{disease_name}", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.get("/api/v1/treatment/{disease_name}/voice/{language}")
async def get_voice(disease_name: str, language: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TREATMENT_URL}/treatment/{disease_name}/voice/{language}", timeout=30
        )
    if resp.headers.get("content-type", "").startswith("audio"):
        return StreamingResponse(io.BytesIO(resp.content), media_type="audio/mpeg")
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


# ── Analytics Service Proxy ──────────────────────────────────────────────────

@app.post("/api/v1/analytics/log")
async def log_event(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{ANALYTICS_URL}/log", json=body, timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.get("/api/v1/analytics/summary/{email}")
async def analytics_summary(email: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ANALYTICS_URL}/summary/{email}", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")


@app.get("/api/v1/analytics/regional")
async def regional_analytics():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ANALYTICS_URL}/regional", timeout=10)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type="application/json")
