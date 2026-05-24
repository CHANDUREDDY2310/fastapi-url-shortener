from app.models.link import Link
from app.services.code_utils import generate_code
from app.services.time_utils import normalize_expires_at


# -------------------------
# CREATE LINK
# -------------------------
def create_link(db, payload):
    link = Link(
        code=generate_code(),
        long_url=payload.long_url,
        expires_at=normalize_expires_at(payload.expires_at)
    )

    db.add(link)
    db.commit()
    db.refresh(link)
    return link


# -------------------------
# GET BY ID
# -------------------------
def get_link_by_id(db, id: int):
    return db.query(Link).filter(Link.id == id).first()


# -------------------------
# LIST ALL LINKS
# -------------------------
def list_links(db):
    return db.query(Link).all()