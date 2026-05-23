from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db, Base, engine
from app.models.link import Link
from app.models.click_event import ClickEvent
from app.schemas.link import CreateLinkRequest
from app.services.links_service import (
    create_link,
    get_link_by_id,
    list_links,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/links")
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
            "tags": link.tags,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/links")
def get_all_links(db: Session = Depends(get_db)):
    try:
        links = list_links(db)

        return links

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/links/{id}")
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

        short_url = f"{request.base_url}r/{link.code}"

        return {
            "id": link.id,
            "code": link.code,
            "short_url": short_url,
            "long_url": link.long_url,
            "expires_at": link.expires_at,
            "tags": link.tags,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/r/{code}")
def redirect(
    code: str,
    user_agent: str = "",
    referrer: str = "",
):
    db = SessionLocal()

    try:
        link = db.query(Link).filter(Link.code == code).first()

        if not link:
            raise HTTPException(
                status_code=404,
                detail=f"Short code '{code}' not found",
            )

        if link.expires_at and link.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=410,
                detail="This short link has expired",
            )

        click = ClickEvent(
            link_id=link.id,
            user_agent=user_agent or "unknown",
            referrer=referrer or "direct",
            ip_hash="",
        )

        db.add(click)
        db.commit()

        return RedirectResponse(
            url=link.long_url,
            status_code=302,
        )

    finally:
        db.close()