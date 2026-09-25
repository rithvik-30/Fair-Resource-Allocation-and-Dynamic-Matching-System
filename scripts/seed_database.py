"""Database seeding script with realistic synthetic data."""

import os
import sys
from datetime import datetime, timedelta, timezone

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from backend.db.session import SessionLocal, engine
from backend.db.base import Base
from backend.db.models import (
    AgencyModel,
    DonationModel,
    DonorModel,
    RescueRequestModel,
    VolunteerModel,
)


def seed():
    """Populates the database with initial synthetic data."""
    print("Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        if db.query(DonorModel).first() is not None:
            print("Database already contains data. Skipping seed.")
            return

        now = datetime.now(timezone.utc)

        # 1. Donors (3)
        donors = [
            DonorModel(
                name="Fresh Market Supermarket",
                organization_type="Supermarket",
                latitude=37.7749,
                longitude=-122.4194,
            ),
            DonorModel(
                name="Bay Area Bakery",
                organization_type="Bakery",
                latitude=37.7833,
                longitude=-122.4167,
            ),
            DonorModel(
                name="Downtown Catering Co",
                organization_type="Caterer",
                latitude=37.7650,
                longitude=-122.4200,
            ),
        ]
        db.add_all(donors)
        db.commit()
        for d in donors:
            db.refresh(d)
        print(f"Seeded {len(donors)} donors.")

        # 2. Donations (4)
        donations = [
            DonationModel(
                donor_id=donors[0].id,
                food_type="Fresh Produce & Apples",
                quantity_kg=150.0,
                available_from=now,
                available_until=now + timedelta(hours=12),
                requires_refrigeration=False,
            ),
            DonationModel(
                donor_id=donors[0].id,
                food_type="Dairy & Yogurt",
                quantity_kg=80.0,
                available_from=now,
                available_until=now + timedelta(hours=6),
                requires_refrigeration=True,
            ),
            DonationModel(
                donor_id=donors[1].id,
                food_type="Artisan Bread & Pastries",
                quantity_kg=50.0,
                available_from=now,
                available_until=now + timedelta(hours=24),
                requires_refrigeration=False,
            ),
            DonationModel(
                donor_id=donors[2].id,
                food_type="Prepared Meals & Soups",
                quantity_kg=120.0,
                available_from=now,
                available_until=now + timedelta(hours=4),
                requires_refrigeration=True,
            ),
        ]
        db.add_all(donations)
        db.commit()
        for dn in donations:
            db.refresh(dn)
        print(f"Seeded {len(donations)} donations.")

        # 3. Agencies (3)
        agencies = [
            AgencyModel(
                name="St. Vincent Food Pantry",
                latitude=37.7750,
                longitude=-122.4180,
                demand_kg=180.0,
                storage_capacity_kg=300.0,
                requires_refrigeration=False,
                priority=2,
            ),
            AgencyModel(
                name="Tenderloin Community Shelter",
                latitude=37.7840,
                longitude=-122.4120,
                demand_kg=120.0,
                storage_capacity_kg=200.0,
                requires_refrigeration=True,
                priority=3,
            ),
            AgencyModel(
                name="Mission Family Haven",
                latitude=37.7590,
                longitude=-122.4150,
                demand_kg=100.0,
                storage_capacity_kg=150.0,
                requires_refrigeration=False,
                priority=1,
            ),
        ]
        db.add_all(agencies)
        db.commit()
        for a in agencies:
            db.refresh(a)
        print(f"Seeded {len(agencies)} agencies.")

        # 4. Volunteers (4)
        volunteers = [
            VolunteerModel(
                name="Alex Rivera",
                latitude=37.7760,
                longitude=-122.4170,
                capacity_kg=100.0,
                has_refrigeration=False,
                available_from=now - timedelta(hours=1),
                available_until=now + timedelta(hours=8),
                current_workload_kg=0.0,
                max_travel_distance_km=25.0,
            ),
            VolunteerModel(
                name="Jordan Chen",
                latitude=37.7800,
                longitude=-122.4150,
                capacity_kg=150.0,
                has_refrigeration=True,
                available_from=now - timedelta(hours=1),
                available_until=now + timedelta(hours=6),
                current_workload_kg=30.0,
                max_travel_distance_km=30.0,
            ),
            VolunteerModel(
                name="Sam Taylor",
                latitude=37.7680,
                longitude=-122.4210,
                capacity_kg=80.0,
                has_refrigeration=False,
                available_from=now,
                available_until=now + timedelta(hours=10),
                current_workload_kg=0.0,
                max_travel_distance_km=15.0,
            ),
            VolunteerModel(
                name="Morgan Vance",
                latitude=37.7600,
                longitude=-122.4100,
                capacity_kg=200.0,
                has_refrigeration=True,
                available_from=now,
                available_until=now + timedelta(hours=12),
                current_workload_kg=0.0,
                max_travel_distance_km=40.0,
            ),
        ]
        db.add_all(volunteers)
        db.commit()
        for v in volunteers:
            db.refresh(v)
        print(f"Seeded {len(volunteers)} volunteers.")

        # 5. Rescue Requests (3)
        requests = [
            RescueRequestModel(
                donation_id=donations[0].id,
                agency_id=agencies[0].id,
                requested_quantity_kg=100.0,
                pickup_deadline=now + timedelta(hours=5),
                status="pending",
            ),
            RescueRequestModel(
                donation_id=donations[1].id,
                agency_id=agencies[1].id,
                requested_quantity_kg=80.0,
                pickup_deadline=now + timedelta(hours=4),
                status="pending",
            ),
            RescueRequestModel(
                donation_id=donations[3].id,
                agency_id=agencies[2].id,
                requested_quantity_kg=60.0,
                pickup_deadline=now + timedelta(hours=3),
                status="pending",
            ),
        ]
        db.add_all(requests)
        db.commit()
        for r in requests:
            db.refresh(r)
        print(f"Seeded {len(requests)} rescue requests.")

        print("Database seed completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
