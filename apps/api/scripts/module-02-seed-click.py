import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.db import SessionLocal
from app.models.link import Link
from app.models.click_event import ClickEvent

CODE = "demo01"


def main() -> None:
    db = SessionLocal()
    try:
        # Get the link first
        link = db.query(Link).filter(Link.code == CODE).first()
        if not link:
            print(f"Link with code={CODE} not found. Run module-02-seed-query.py first.")
            return

        # Check if click events already exist
        existing_clicks = db.query(ClickEvent).filter(
            ClickEvent.link_id == link.id
        ).count()
        
        if existing_clicks == 0:
            # Create sample click events
            now = datetime.utcnow()
            sample_clicks = [
                ClickEvent(
                    link_id=link.id,
                    clicked_at=now - timedelta(hours=2),
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    referrer="https://google.com",
                    ip_hash="hash_001",
                ),
                ClickEvent(
                    link_id=link.id,
                    clicked_at=now - timedelta(hours=1),
                    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14)",
                    referrer="https://twitter.com",
                    ip_hash="hash_002",
                ),
                ClickEvent(
                    link_id=link.id,
                    clicked_at=now,
                    user_agent="Mozilla/5.0 (X11; Linux x86_64)",
                    referrer="https://linkedin.com",
                    ip_hash="hash_003",
                ),
            ]
            db.add_all(sample_clicks)
            db.commit()
            print(f"inserted {len(sample_clicks)} click events for code={CODE}")

        # Query and display click events
        clicks = db.query(ClickEvent).filter(
            ClickEvent.link_id == link.id
        ).order_by(ClickEvent.clicked_at).all()
        
        print(f"selected {len(clicks)} click events for code={CODE}")
        for click in clicks:
            print(f"  clicked_at={click.clicked_at}, referrer={click.referrer}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
