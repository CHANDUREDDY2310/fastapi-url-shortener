import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import SessionLocal
from app.models.link import Link

CODE = "demo01"
LONG_URL = "https://example.com"


def main() -> None:
    db = SessionLocal()
    try:
        if not db.query(Link).filter(Link.code == CODE).first():
            db.add(
                Link(
                    code=CODE,
                    long_url=LONG_URL,
                    created_by="seed-script",
                )
            )
            db.commit()
            print(f"inserted code={CODE}")

        row = db.query(Link).filter(Link.code == CODE).one()
        print(f"selected code={row.code}")
        print(f"matched long_url={row.long_url}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
