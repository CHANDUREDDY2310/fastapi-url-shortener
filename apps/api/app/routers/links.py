from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.link import CreateLinkRequest
from app.services.links_service import (
    create_link,
    get_link_by_id,
    list_links,
)

router = APIRouter(prefix="/links", tags=["links"])


@router.post("")
def create_short_link(
    payload: CreateLinkRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        link = create_link(db, payload)

        short_url = f"{request.base_url}r/{link.code}"

        return {
            "id": link.id,
            "code": link.code,
            "short_url": short_url,
            "long_url": link.long_url,
            "expires_at": link.expires_at,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def get_all_links(db: Session = Depends(get_db)):
    try:
        return list_links(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}")
def get_single_link(id: int, request: Request, db: Session = Depends(get_db)):
    link = get_link_by_id(db, id)

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    short_url = f"{request.base_url}r/{link.code}"

    return {
        "id": link.id,
        "code": link.code,
        "short_url": short_url,
        "long_url": link.long_url,
        "expires_at": link.expires_at,
    }