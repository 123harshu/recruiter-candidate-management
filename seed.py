"""Idempotent seed script inserting 12 realistic candidates with varying stage ages."""
from datetime import datetime, timedelta, timezone
from app.database import SessionLocal, Base, engine
from app.models import Candidate, CandidateStageHistory


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Candidate).first() is not None:
            print("Database already contains seed data. Skipping seed.")
            return

        print("Seeding database with realistic candidate profiles...")
        now = datetime.now(timezone.utc)

        # 12 Realistic Candidate profiles
        candidates_data = [
            # Applied
            ("Harshita Verma", "harshita.v@example.com", "+1-555-0101", "Senior Full-Stack Engineer", "LinkedIn", "Applied", 1),
            ("Aarav Sharma", "aarav.s@example.com", "+1-555-0102", "Backend Python Developer", "Direct", "Applied", 3),
            ("Priya Patel", "priya.p@example.com", "+1-555-0103", "Data Scientist", "Referral", "Applied", 0),
            
            # Screening
            ("Rahil Kapoor", "rahil.k@example.com", "+1-555-0104", "Product Manager", "LinkedIn", "Screening", 10),
            ("Neha Gupta", "neha.g@example.com", "+1-555-0105", "Frontend Engineer", "Recruiter Outreach", "Screening", 2),
            
            # Interview
            ("Rahul Nair", "rahul.n@example.com", "+1-555-0106", "DevOps Specialist", "LinkedIn", "Interview", 8),
            ("Ananya Rao", "ananya.r@example.com", "+1-555-0107", "Senior Python Engineer", "Referral", "Interview", 2),
            ("Vikram Singh", "vikram.s@example.com", "+1-555-0108", "System Architect", "Direct", "Interview", 6),

            # Offer
            ("Rohan Mehta", "rohan.m@example.com", "+1-555-0109", "Engineering Manager", "Recruiter Outreach", "Offer", 4),
            ("Sanya Malhotra", "sanya.m@example.com", "+1-555-0110", "UX Designer", "LinkedIn", "Offer", 1),

            # Hired
            ("Devika Joshi", "devika.j@example.com", "+1-555-0111", "Backend Lead", "Referral", "Hired", 15),
            ("Karan Kumar", "karan.k@example.com", "+1-555-0112", "QA Automation Engineer", "Direct", "Hired", 20),
        ]

        stage_progression = ["Applied", "Screening", "Interview", "Offer", "Hired"]

        for name, email, phone, position, source, target_stage, days_in_stage in candidates_data:
            updated_at = now - timedelta(days=days_in_stage)
            created_at = updated_at - timedelta(days=5)

            c = Candidate(
                full_name=name,
                email=email,
                phone=phone,
                position=position,
                source=source,
                current_stage=target_stage,
                created_at=created_at,
                updated_at=updated_at
            )
            db.add(c)
            db.flush()

            # Build stage history up to current target_stage
            target_idx = stage_progression.index(target_stage)
            from_st = None

            for idx in range(target_idx + 1):
                curr_st = stage_progression[idx]
                h_time = created_at + timedelta(hours=idx * 6)
                
                hist = CandidateStageHistory(
                    candidate_id=c.id,
                    from_stage=from_st,
                    to_stage=curr_st,
                    changed_at=h_time,
                    changed_by="system" if idx == 0 else "Recruiter Admin",
                    reason="Candidate initial registration" if idx == 0 else f"Passed {from_st} review"
                )
                db.add(hist)
                from_st = curr_st

        db.commit()
        print("Database seeded successfully with 12 candidates and complete stage histories.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()