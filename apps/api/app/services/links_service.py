import random
import string

from sqlalchemy.orm import Session

from app.models.link import Link

BASE62_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6


def generate_base62_code(length: int = CODE_LENGTH) -> str:
    return "".join(random.choices(BASE62_ALPHABET, k=length))


def generate_unique_code(db: Session) -> str:
    while True:
        code = generate_base62_code()

        existing = db.query(Link).filter(Link.code == code).first()

        if not existing:
            return code


def create_link(db: Session, payload):
    generated_code = generate_unique_code(db)

    link = Link(
        code=generated_code,
        long_url=payload.long_url,
        expires_at=payload.expires_at,
        tags=payload.tags,
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    return link


def get_link_by_id(db: Session, link_id: int):
    return db.query(Link).filter(Link.id == link_id).first()


def get_link_by_code(db: Session, code: str):
    return db.query(Link).filter(Link.code == code).first()


def list_links(db: Session):
    return db.query(Link).all()