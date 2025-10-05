from fastapi import FastAPI
from src.users_api import router as users_router
from src.hazard_api import router as hazard_router

app = FastAPI(title="Transit API")

app.include_router(users_router)
app.include_router(hazard_router)


@app.get("/")
def root():
    return {"ok": True, "service": "micro_service"}

@app.get("/_ah/health")
def health():
    return {"status": "ok"}
