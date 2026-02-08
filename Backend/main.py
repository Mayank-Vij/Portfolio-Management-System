# ============================================================
# main.py — Financial Dashboard Backend (Modular Architecture)
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import modular routers
from analytics import router as analytics_router     # your core analytics routes
from auth import router as auth_router               # login/signup JWT auth
from realtime import router as realtime_router       # websocket live data
from finlearn import router as finlearn_router       # learning platform (LMS-style)

# ------------------------------------------------------------
# APP INITIALIZATION
# ------------------------------------------------------------
app = FastAPI(title="SmartGrow Pro Backend (Next-Gen Financial Dashboard)")

# Enable CORS for frontend connection (React, HTML, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev: allow all, in prod restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# ROUTER REGISTRATION
# ------------------------------------------------------------
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics & ML"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(realtime_router, prefix="/realtime", tags=["Realtime Data"])
app.include_router(finlearn_router, prefix="/finlearn", tags=["Financial Learning"])

# ------------------------------------------------------------
# ROOT ENDPOINT
# ------------------------------------------------------------
@app.get("/")
def root():
    """
    Root health check endpoint
    """
    return {
        "message": "🚀 SmartGrow Pro Financial Dashboard API is running successfully!",
        "modules": [
            "/analytics → stock, ML, risk, PCA, indicators",
            "/auth → user login/signup",
            "/realtime → live WebSocket data",
            "/finlearn → educational platform",
        ]
    }

# ------------------------------------------------------------
# STATIC FILE MOUNTS (plots, reports, etc.)
# ------------------------------------------------------------
# Serve plots directory (ensure it exists)
app.mount("/plots", StaticFiles(directory="plots"), name="plots")

# Serve dataset files if needed
app.mount("/dataset", StaticFiles(directory="dataset"), name="dataset")

# ------------------------------------------------------------
# MAIN ENTRY POINT (for local VSCode run)
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
