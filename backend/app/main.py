import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    from app.database import Base, engine  # noqa: F811
    import app.auth.models  # noqa: F401
    import app.conversations.models  # noqa: F401
    import app.devices.models  # noqa: F401
    import app.finance.models  # noqa: F401
    import app.fitness.models  # noqa: F401
    import app.memory.models  # noqa: F401
    import app.study.models  # noqa: F401
    import app.tasks.models  # noqa: F401

    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

if STATIC_DIR.is_dir():
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")
