from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.config import settings
from app.conversations.router import router as conv_router
from app.dashboard.router import router as dash_router
from app.devices.router import router as dev_router
from app.finance.router import router as fin_router
from app.fitness.router import router as fit_router
from app.memory.router import router as mem_router
from app.study.router import router as study_router
from app.tasks.router import router as tasks_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(conv_router)
app.include_router(tasks_router)
app.include_router(mem_router)
app.include_router(fit_router)
app.include_router(fin_router)
app.include_router(study_router)
app.include_router(dev_router)
app.include_router(dash_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.VERSION}
