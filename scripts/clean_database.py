"""
Utility script to clear operational data from the database.

Removes: ReferenceRequest, TimeSlots, Applications, Position records (in a safe order).
Usage (from repo root):
    python -m scripts.clean_database
"""

import sqlalchemy as sqla

from config import Config
from app import create_app, db
from app.main.models import Applications, Position, ReferenceRequest, TimeSlots

app = create_app(Config)

def clear_data() -> None:
    """Delete dependent records in foreign-key order."""
    with app.app_context():
        db.session.execute(sqla.delete(ReferenceRequest))
        db.session.execute(sqla.delete(TimeSlots))
        db.session.execute(sqla.delete(Applications))
        db.session.execute(sqla.delete(Position))
        db.session.commit()
        print("Cleared reference requests, time slots, applications, and positions.")


if __name__ == "__main__":
    clear_data()