import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_verify import router as verify_router
from api.routes_history import router as history_router
from api.middleware import setup_middleware
from db.database import connect_to_mongo


app = FastAPI(title="Gurisan Trengkas AI Backend")


# -----------------------------
# CORS (benarkan frontend akses)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aca boleh ketatkan kemudian ikut domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Middleware custom (logging, error handling, dsb.)
# -----------------------------
# Fungsi setup_middleware akan ditakrifkan dalam api/middleware.py
setup_middleware(app)


# -----------------------------
# Endpoint Root (Health Check)
# -----------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Gurisan Trengkas AI backend is running.",
    }


# -----------------------------
# Endpoint: Status Server
# -----------------------------
@app.get("/api/status")
async def status():
    return {
        "status": "ok",
        "message": "Gurisan Trengkas AI backend is running.",
    }


# -----------------------------
# Sambung ke MongoDB semasa server mula
# -----------------------------
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


# -----------------------------
# Daftarkan semua route API
# -----------------------------
# routes_verify akan menyediakan /verify
# routes_history akan menyediakan /history
app.include_router(verify_router, prefix="/api")
app.include_router(history_router, prefix="/api")


# -----------------------------
# Run server (untuk local testing)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Aca boleh set reload=True jika develop secara lokal
    # tetapi untuk production/Heroku, biarkan False
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
