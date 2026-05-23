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

        short_url = f"{request.base_url}r/{link.short_code}"

        return {
            "id": link.id,
            "short_code": link.short_code,
            "short_url": short_url,
            "long_url": link.long_url,
            "expires_at": link.expires_at,
            "tags": link.tags,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create short link",
        )


@router.get("")
def get_all_links(db: Session = Depends(get_db)):
    try:
        links = list_links(db)

        return links

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch links",
        )


@router.get("/{id}")
def get_single_link(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        link = get_link_by_id(db, id)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="Link not found",
            )

        short_url = f"{request.base_url}r/{link.short_code}"

        return {
            "id": link.id,
            "short_code": link.short_code,
            "short_url": short_url,
            "long_url": link.long_url,
            "expires_at": link.expires_at,
            "tags": link.tags,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch link",
        )