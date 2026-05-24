from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.db import get_db
from app.models.link import Link
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/r/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()

    if not link:
        logger.error("link not found")
        raise HTTPException(status_code=404, detail="Link not found")

    return RedirectResponse(url=link.long_url)