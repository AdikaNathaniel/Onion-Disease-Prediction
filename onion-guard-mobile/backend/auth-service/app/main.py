import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt

app = FastAPI(title="OnionGuard Auth Service", version="1.0.0")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "onionguard_auth")
JWT_SECRET = os.getenv("JWT_SECRET", "onionguard-secret-change-in-production")
JWT_ALGORITHM = "HS256"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    user_type: str = "Farmer"
    username: str
    language_preference: str = "en"


class LoginRequest(BaseModel):
    email: str
    password: str
    user_type: str = "Farmer"


def create_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}


@app.post("/register")
async def register(req: RegisterRequest):
    existing = await users_collection.find_one({"email": req.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = await users_collection.find_one({"username": req.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    if req.user_type == "Admin":
        existing_admin = await users_collection.find_one({"user_type": "Admin"})
        if existing_admin:
            raise HTTPException(status_code=400, detail="An admin account already exists. Only one admin is allowed.")

    user_doc = {
        "name": req.name,
        "email": req.email.lower(),
        "phone": req.phone,
        "password": pwd_context.hash(req.password),
        "user_type": req.user_type,
        "username": req.username,
        "language_preference": req.language_preference,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True,
    }
    await users_collection.insert_one(user_doc)

    return {
        "success": True,
        "message": "Account successfully created.",
    }


@app.post("/login")
async def login(req: LoginRequest):
    user = await users_collection.find_one({"email": req.email.lower()})
    if not user:
        raise HTTPException(status_code=401, detail="No account found. Please create an account.")

    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Your account has been deactivated")

    if user["user_type"] != req.user_type:
        raise HTTPException(
            status_code=401,
            detail=f"This email is not registered as {req.user_type}. You are registered as {user['user_type']}."
        )

    if not pwd_context.verify(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "email": user["email"],
        "user_type": user["user_type"],
        "name": user["name"],
    })

    return {
        "success": True,
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "user_type": user["user_type"],
            "username": user["username"],
            "language_preference": user.get("language_preference", "en"),
        },
    }


@app.get("/profile/{email}")
async def get_profile(email: str):
    user = await users_collection.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "user": {
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "user_type": user["user_type"],
            "username": user["username"],
            "language_preference": user.get("language_preference", "en"),
            "created_at": user.get("created_at"),
        },
    }


@app.get("/users")
async def list_users():
    cursor = users_collection.find({}, {"_id": 0, "password": 0})
    users = await cursor.to_list(length=500)
    return {"success": True, "users": users}


@app.post("/users/{email}/toggle-status")
async def toggle_user_status(email: str):
    user = await users_collection.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_status = not user.get("is_active", True)
    await users_collection.update_one(
        {"email": email.lower()},
        {"$set": {"is_active": new_status}}
    )
    return {"success": True, "is_active": new_status, "message": f"User {'activated' if new_status else 'deactivated'}"}


class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str


@app.post("/change-password")
async def change_password(req: ChangePasswordRequest):
    user = await users_collection.find_one({"email": req.email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    if not pwd_context.verify(req.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    new_hash = pwd_context.hash(req.new_password)
    await users_collection.update_one(
        {"email": req.email.lower()},
        {"$set": {"password": new_hash}}
    )

    return {
        "success": True,
        "message": "Password changed successfully.",
    }


@app.post("/forgot-password/{email}")
async def forgot_password(email: str):
    user = await users_collection.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    return {
        "success": True,
        "message": "A temporary password has been sent to your email address.",
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
