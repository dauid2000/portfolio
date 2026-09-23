"""Seeds initial data on startup: admin account, profile, skills,
projects, education and services.

Seeding is idempotent — rows are inserted only when the relevant table
is empty, so restarts never duplicate content.
"""
from sqlalchemy.orm import Session

from config import settings
from database import SessionLocal
from models.admin import Admin
from models.education import Education
from models.profile import Profile
from models.project import Project
from models.service import Service
from models.skill import Skill
from security import hash_password

PROFILE = dict(
    name="David Musumali",
    profession="Third-Year Mining Engineering Student",
    university="The Copperbelt University",
    email="DMUSUMALI01@GMAIL.COM",
    phone="+260773108622",
    alt_phone="+260761031385",
    location="Zambia",
    bio=(
        "Mining Engineering student combining engineering knowledge with software "
        "development, AI, databases, automation and data analysis to build practical "
        "solutions for real operational problems."
    ),
)

SKILLS = [
    ("Python Programming", "Programming"),
    ("Web Development", "Software Development"),
    ("SQL", "Databases"),
    ("SQLite", "Databases"),
    ("Database Design", "Databases"),
    ("Database Management", "Databases"),
    ("Database Security", "Databases"),
    ("AI", "Technology"),
    ("Automation", "Technology"),
    ("Data Analysis", "Data"),
    ("LaTeX", "Productivity"),
    ("Microsoft Office", "Productivity"),
    ("Software Development", "Software Development"),
    ("Engineering Design", "Engineering"),
]

PROJECTS = [
    dict(
        name="Bana Kulu Finances",
        description=(
            "A loan business management system for managing customers, loans, "
            "repayments, interest, overdue loans, reports, and business records."
        ),
        tagline=None,
        technologies="Python, Streamlit, SQLite",
    ),
    dict(
        name="Bus Station Transport Management & Automated Dispatch System",
        description=(
            "An automated transport management and dispatch system designed to manage "
            "buses, routes, loading sequences, daily fleet allocation, breakdowns, "
            "standby buses, and dispatch operations."
        ),
        tagline=None,
        technologies="Python, SQLite, Automation",
    ),
    dict(
        name="KITE",
        description=(
            "A technology and engineering concept focused on software development, AI, "
            "automation, databases, engineering solutions, and digital services."
        ),
        tagline="Engineering Ideas. Building the Future.",
        technologies="Software Development, AI, Automation, Databases",
    ),
]

EDUCATION = [
    dict(
        institution="The Copperbelt University",
        programme="Mining Engineering",
        level="Third Year",
        status="Currently Studying",
    ),
]

SERVICES = [
    ("Python Programming", "Clean, practical Python programs and scripts for engineering and business tasks."),
    ("Software Development", "Web and desktop applications designed around real user and operational needs."),
    ("AI & Automation", "Intelligent, automated workflows that remove repetitive manual work."),
    ("Database Design & Management", "Well-structured SQL and SQLite databases built for reliability and growth."),
    ("Database Security", "Secure data storage practices that protect records and sensitive business information."),
    ("Data Analysis & Reporting", "Turning raw operational data into clear reports and informed decisions."),
    ("Engineering Technology Solutions", "Technology applied to engineering problems — from mine operations to field work."),
]


def seed_initial_data() -> None:
    db: Session = SessionLocal()
    try:
        if db.query(Admin).count() == 0:
            db.add(Admin(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
            ))

        if db.query(Profile).count() == 0:
            db.add(Profile(**PROFILE))

        if db.query(Skill).count() == 0:
            db.add_all([Skill(name=name, category=cat) for name, cat in SKILLS])

        if db.query(Project).count() == 0:
            db.add_all([Project(**p) for p in PROJECTS])

        if db.query(Education).count() == 0:
            db.add_all([Education(**e) for e in EDUCATION])

        if db.query(Service).count() == 0:
            db.add_all([Service(title=t, description=d) for t, d in SERVICES])

        db.commit()
    finally:
        db.close()
