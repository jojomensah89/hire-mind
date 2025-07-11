import uuid
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.base import Base
from app.db.models.user import User
from app.db.models.organization import Organization
from app.db.models.job_listing import JobListing
from app.db.models.job_listing_application import JobListingApplication
from app.db.models.user_notification_settings import UserNotificationSettings
from app.db.models.user_resume import UserResume
from app.db.models.organization_user_settings import OrganizationUserSettings
from app.db.enums import (
    JobListingType, ExperienceLevel, ApplicationStage,
    WageInterval, LocationRequirement, JobListingStatus
)


def create_all_tables(db: Session):
    """Create all database tables. Use migrations in production."""
    print("Creating database tables...")
    Base.metadata.drop_all(bind=db.bind)
    Base.metadata.create_all(bind=db.bind)
    print("Tables created successfully.")


def seed_data(db: Session):
    print("Seeding data...")

    # Seed Users
    user1 = User(
        id=str(uuid.uuid4()),
        name="Alice Smith",
        email="alice@example.com",
        image_url="http://example.com/alice.jpg"
    )
    user2 = User(
        id=str(uuid.uuid4()),
        name="Bob Johnson",
        email="bob@example.com",
        image_url="http://example.com/bob.jpg"
    )
    user3 = User(
        id=str(uuid.uuid4()),
        name="Carol Davis",
        email="carol@example.com",
        image_url="http://example.com/carol.jpg"
    )

    db.add_all([user1, user2, user3])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    db.refresh(user3)
    print(f"Seeded users: {user1.name}, {user2.name}, {user3.name}")

    # Seed Organizations
    org1 = Organization(
        id=str(uuid.uuid4()),
        name="Tech Solutions Inc.",
        image_url="http://example.com/techsolutions.jpg"
    )
    org2 = Organization(
        id=str(uuid.uuid4()),
        name="Creative Minds LLC",
        image_url="http://example.com/creativeminds.jpg"
    )
    org3 = Organization(
        id=str(uuid.uuid4()),
        name="Data Analytics Corp",
        image_url="http://example.com/dataanalytics.jpg"
    )

    db.add_all([org1, org2, org3])
    db.commit()
    db.refresh(org1)
    db.refresh(org2)
    db.refresh(org3)
    print(f"Seeded organizations: {org1.name}, {org2.name}, {org3.name}")

    # Seed Job Listings
    job1 = JobListing(
        id=str(uuid.uuid4()),
        title="Senior Software Engineer",
        description="Develop and maintain web applications using modern frameworks. Work with cross-functional teams to deliver high-quality software solutions.",
        organization_id=org1.id,
        type=JobListingType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        wage=120000,
        wage_interval=WageInterval.YEARLY,
        location_requirement=LocationRequirement.REMOTE,
        status=JobListingStatus.PUBLISHED,
        is_featured=True,
        city="San Francisco",
        state_abbreviation="CA",
        posted_at=datetime.now()
    )

    job2 = JobListing(
        id=str(uuid.uuid4()),
        title="UX Designer",
        description="Design user interfaces for mobile and web applications. Collaborate with product managers and developers to create intuitive user experiences.",
        organization_id=org2.id,
        type=JobListingType.FULL_TIME,
        experience_level=ExperienceLevel.MID_LEVEL,
        wage=85000,
        wage_interval=WageInterval.YEARLY,
        location_requirement=LocationRequirement.HYBRID,
        status=JobListingStatus.PUBLISHED,
        is_featured=False,
        city="New York",
        state_abbreviation="NY",
        posted_at=datetime.now()
    )

    job3 = JobListing(
        id=str(uuid.uuid4()),
        title="Data Analyst Intern",
        description="Analyze large datasets and create visualizations to support business decisions. Perfect opportunity for students or recent graduates.",
        organization_id=org3.id,
        type=JobListingType.INTERNSHIP,
        experience_level=ExperienceLevel.JUNIOR,
        wage=25,
        wage_interval=WageInterval.HOURLY,
        location_requirement=LocationRequirement.IN_OFFICE,
        status=JobListingStatus.PUBLISHED,
        is_featured=False,
        city="Chicago",
        state_abbreviation="IL",
        posted_at=datetime.now()
    )

    job4 = JobListing(
        id=str(uuid.uuid4()),
        title="Frontend Developer",
        description="Build responsive web applications using React and TypeScript. Work in a collaborative environment with designers and backend developers.",
        organization_id=org1.id,
        type=JobListingType.PART_TIME,
        experience_level=ExperienceLevel.MID_LEVEL,
        wage=75000,
        wage_interval=WageInterval.YEARLY,
        location_requirement=LocationRequirement.REMOTE,
        status=JobListingStatus.DRAFT,
        is_featured=False,
        city="Austin",
        state_abbreviation="TX"
    )

    db.add_all([job1, job2, job3, job4])
    db.commit()
    db.refresh(job1)
    db.refresh(job2)
    db.refresh(job3)
    db.refresh(job4)
    print(f"Seeded job listings: {job1.title}, {job2.title}, {job3.title}, {job4.title}")

    # Seed User Notification Settings
    user1_notifications = UserNotificationSettings(
        user_id=user1.id,
        new_job_email_notifications=True,
        ai_prompt="Find me software engineering jobs in tech companies"
    )
    user2_notifications = UserNotificationSettings(
        user_id=user2.id,
        new_job_email_notifications=False,
        ai_prompt="Looking for design roles in creative agencies"
    )
    user3_notifications = UserNotificationSettings(
        user_id=user3.id,
        new_job_email_notifications=True,
        ai_prompt="Entry-level data analysis positions"
    )

    db.add_all([user1_notifications, user2_notifications, user3_notifications])
    db.commit()
    print("Seeded user notification settings")

    # Seed User Resumes
    user1_resume = UserResume(
        user_id=user1.id,
        resume_file_url="https://example.com/resumes/alice_smith_resume.pdf",
        resume_file_key="resumes/alice_smith_resume.pdf",
        ai_summary="Experienced software engineer with 5+ years in full-stack development"
    )
    user2_resume = UserResume(
        user_id=user2.id,
        resume_file_url="https://example.com/resumes/bob_johnson_resume.pdf",
        resume_file_key="resumes/bob_johnson_resume.pdf",
        ai_summary="Creative UX designer with expertise in mobile and web design"
    )

    db.add_all([user1_resume, user2_resume])
    db.commit()
    print("Seeded user resumes")

    # Seed Organization User Settings
    org_user_settings1 = OrganizationUserSettings(
        user_id=user1.id,
        organization_id=org1.id,
        new_application_email_notifications=True,
        minimum_rating=4
    )
    org_user_settings2 = OrganizationUserSettings(
        user_id=user2.id,
        organization_id=org2.id,
        new_application_email_notifications=False,
        minimum_rating=3
    )

    db.add_all([org_user_settings1, org_user_settings2])
    db.commit()
    print("Seeded organization user settings")

    # Seed Job Applications
    app1 = JobListingApplication(
        job_listing_id=job1.id,
        user_id=user2.id,
        cover_letter="I am passionate about software development and have extensive experience with modern web technologies. I would love to contribute to your team's success.",
        stage=ApplicationStage.APPLIED,
        rating=5
    )
    app2 = JobListingApplication(
        job_listing_id=job2.id,
        user_id=user1.id,
        cover_letter="While my background is in software engineering, I have a strong interest in UX design and have been developing my skills in this area.",
        stage=ApplicationStage.INTERESTED,
        rating=4
    )
    app3 = JobListingApplication(
        job_listing_id=job3.id,
        user_id=user3.id,
        cover_letter="As a recent graduate in data science, I am eager to apply my analytical skills in a practical setting. This internship would be perfect for my career goals.",
        stage=ApplicationStage.INTERVIEWED,
        rating=5
    )
    app4 = JobListingApplication(
        job_listing_id=job1.id,
        user_id=user3.id,
        cover_letter="I am transitioning into software engineering and believe my analytical background would be valuable for your team.",
        stage=ApplicationStage.DENIED,
        rating=3
    )

    db.add_all([app1, app2, app3, app4])
    db.commit()
    print("Seeded job applications")

    print("Data seeding complete!")
    print("\nSummary:")
    print(f"- {db.query(User).count()} users")
    print(f"- {db.query(Organization).count()} organizations")
    print(f"- {db.query(JobListing).count()} job listings")
    print(f"- {db.query(JobListingApplication).count()} job applications")
    print(f"- {db.query(UserNotificationSettings).count()} user notification settings")
    print(f"- {db.query(UserResume).count()} user resumes")
    print(f"- {db.query(OrganizationUserSettings).count()} organization user settings")


if __name__ == "__main__":
    db: Session = SessionLocal()
    try:
        # Ensure tables are created before seeding
        create_all_tables(db)
        seed_data(db)
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
        raise
    finally:
        db.close()