import logging
from fastapi import FastAPI

from app.config import settings
from app.routers.links import router as links_router
from app.routers.redirect import router as redirect_router

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("request received")

    response = await call_next(request)

    logger.info("response sent")

    return response


# register routers
app.include_router(links_router)
app.include_router(redirect_router)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/live")
def live():
    return {"status": "alive"}


@app.get("/ready")
def ready():
    return {"status": "ready"}