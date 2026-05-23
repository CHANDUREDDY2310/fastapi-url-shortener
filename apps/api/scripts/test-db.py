import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

print("Starting test...")

try:
    from app.db import SessionLocal
    print("✓ Imported SessionLocal")
    
    from app.models.link import Link
    print("✓ Imported Link model")
    
    from app.models.click_event import ClickEvent
    print("✓ Imported ClickEvent model")
    
    db = SessionLocal()
    print("✓ Created database session")
    
    # Query links
    links = db.query(Link).all()
    print(f"✓ Found {len(links)} links")
    for link in links:
        print(f"  - {link.code}: {link.long_url}")
    
    # Query click events
    clicks = db.query(ClickEvent).all()
    print(f"✓ Found {len(clicks)} click events")
    
    db.close()
    print("✓ Test complete!")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
