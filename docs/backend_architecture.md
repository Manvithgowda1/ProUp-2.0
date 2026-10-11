# Proup Backend Architecture & Design Document

> **Project:** Proup (Professional Upgrade)  
> **Backend Engine:** FastAPI (Python 3.12+)  
> **ORM & Database:** SQLAlchemy 2.0 (Async) + PostgreSQL (with SQLite support for local rapid dev)  
> **Migration Manager:** Alembic  
> **Validation & Serialization:** Pydantic v2  

---

## 1. Architectural Principles & Overview

Proup's backend is structured as a **Layered Modular Monolith** with clear separation of concerns, high cohesion, and low coupling. This architecture matches a solo-developer workflow: rapid to iterate, straightforward to maintain, and readily scalable.

```
                    ┌─────────────────────────────────────────┐
                    │          FastAPI Routers (HTTP)         │
                    │   /auth  /events  /students  /admin ... │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │      Dependencies & Middleware Layer    │
                    │   JWT Auth, RBAC Guards, DB Session     │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │          Business Logic Layer           │
                    │   EventService, RecommendationEngine,   │
                    │   AssessmentEvaluator, ShortlistManager │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │       Data Access Layer (SQLAlchemy)    │
                    │   Async Repositories, Declarative Models│
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │          PostgreSQL Database            │
                    │     22 Tables, Relational Integrity     │
                    └─────────────────────────────────────────┘
```

---

## 2. Directory Structure (`/server`)

```text
server/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application factory & router registration
│   │
│   ├── core/                       # Core system configuration & security
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic Settings (ENV variables, DB URL, JWT secrets)
│   │   ├── database.py             # Async SQLAlchemy Engine & SessionLocal
│   │   ├── security.py             # Password hashing (bcrypt) & JWT token utilities
│   │   ├── exceptions.py           # Custom API exceptions & error handlers
│   │   └── logging.py              # Structured application logger
│   │
│   ├── api/                        # HTTP API layer
│   │   ├── __init__.py
│   │   ├── deps.py                 # Dependency injectors (get_db, get_current_user, require_role)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api_router.py       # Aggregator router for all v1 domain routers
│   │       ├── auth.py             # /auth (login, register student, register organizer)
│   │       ├── students.py         # /students (profile, skills, resume)
│   │       ├── organizers.py       # /organizers (organization profiles)
│   │       ├── events.py           # /events (browse, recommendations, CRUD)
│   │       ├── registrations.py    # /registrations (event signup, attendance)
│   │       ├── rounds.py           # /rounds (round 1/2/3 configuration)
│   │       ├── assessments.py      # /assessments (MCQ, questions, answers, submit)
│   │       ├── coding.py           # /coding (problems, test cases, submissions)
│   │       ├── interviews.py       # /interviews (scheduling, feedback)
│   │       ├── shortlists.py       # /shortlists (round qualifications)
│   │       ├── achievements.py     # /achievements (badges, verified certificates)
│   │       ├── hiring.py           # /hiring (job offers, accept/reject)
│   │       ├── admin.py            # /admin (organizer verify, event moderation, analytics)
│   │       ├── notifications.py    # /notifications
│   │       └── blogs.py            # /blogs
│   │
│   ├── models/                     # SQLAlchemy 2.0 Declarative ORM models (22 tables)
│   │   ├── __init__.py
│   │   ├── base.py                 # DeclarativeBase with common TimestampMixin
│   │   ├── user.py                 # users, organizer_profiles, student_profiles
│   │   ├── organization.py         # organizations, colleges
│   │   ├── skill.py                # skills, student_skills
│   │   ├── event.py                # events, event_registrations
│   │   ├── round.py                # event_rounds, round_shortlists, event_results
│   │   ├── assessment.py           # assessments, questions, question_options, answers, assessment_results
│   │   ├── coding.py               # coding_problems, coding_test_cases, coding_submissions
│   │   ├── interview.py            # interviews
│   │   ├── achievement.py          # achievements, student_achievements
│   │   ├── hiring.py               # hiring
│   │   ├── notification.py         # notifications
│   │   └── blog.py                 # blogs
│   │
│   ├── schemas/                    # Pydantic v2 validation models
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── organizer.py
│   │   ├── event.py
│   │   ├── round.py
│   │   ├── assessment.py
│   │   ├── coding.py
│   │   ├── interview.py
│   │   ├── achievement.py
│   │   ├── hiring.py
│   │   ├── admin.py
│   │   ├── notification.py
│   │   └── common.py               # Generic API response envelope, pagination schemas
│   │
│   └── services/                   # Business logic and computations
│       ├── __init__.py
│       ├── recommendation.py       # Skill-overlap matching algorithm
│       ├── assessment_evaluator.py # MCQ auto-grader with negative marking
│       ├── coding_runner.py        # Code execution & test case verification
│       ├── shortlist_service.py    # Cutoff scoring and round advancement
│       └── notification_service.py # Event triggers -> in-app notification records
│
├── alembic/                        # Database migration scripts
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini                     # Alembic configuration
├── tests/                          # Automated Pytest suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_events.py
│   └── test_assessments.py
├── .env.example                    # Sample environment variables
├── Dockerfile                      # Production container image
├── docker-compose.yml              # PostgreSQL + FastAPI local container orchestration
├── pyproject.toml                  # Project packaging & dependencies
└── requirements.txt                # Pip requirements file
```

---

## 3. Core Technical Decisions

### 3.1 Framework: FastAPI
- **Asynchronous natively (`async`/`await`):** High throughput for concurrent students taking tests and viewing live leaderboards.
- **Auto-generated OpenAPI Docs:** Interactive Swagger UI at `/docs` and ReDoc at `/redoc`, facilitating frontend-backend collaboration.
- **Pydantic v2:** Fast Rust-backed schema validation and serialization.

### 3.2 ORM & Database: SQLAlchemy 2.0 Async
- Utilizes `asyncpg` driver for PostgreSQL (`postgresql+asyncpg://user:pass@host:5432/db`).
- Supports `aiosqlite` driver for zero-config lightweight local development (`sqlite+aiosqlite:///./proup.db`).
- Clean separation between declarative models (`app/models/`) and data transfer objects (`app/schemas/`).

### 3.3 Authentication & Role-Based Access Control (RBAC)
- Password hashing using `bcrypt` (or `argon2`).
- Stateless authentication using JWT tokens with HMAC-SHA256 (`HS256`).
- Role enforcement via FastAPI dependencies:
  - `get_current_user`: Extracts and verifies JWT bearer token.
  - `require_role(["student"])`: Ensures role matches.
  - `require_verified_organizer`: Ensures `user.role == "organizer"` AND `organizer_profile.verification_status == "APPROVED"`.
  - `require_admin`: Ensures `user.role == "admin"`.

---

## 4. Business Logic Services Design

### 4.1 Skill-Based Recommendation Engine (`app/services/recommendation.py`)
- **Objective:** Match students with events relevant to their verified and self-declared skills.
- **Algorithm (MVP Scope):**
  1. Retrieve student's skills: `S_student = {skill_id_1, skill_id_2, ...}` with weights $w \in \{1.0 \text{ (Beginner)}, 1.5 \text{ (Intermediate)}, 2.0 \text{ (Advanced)}\}$.
  2. Map event focus skills: derived from event categories and coding/assessment problem tags $S_{event}$.
  3. Calculate Weighted Jaccard Similarity:
     $$\text{Score} = \frac{\sum_{s \in S_{\text{student}} \cap S_{\text{event}}} w_s}{\sum_{s \in S_{\text{student}} \cup S_{\text{event}}} w_s}$$
  4. Rank upcoming events by match score descending.

### 4.2 Assessment Evaluator Service (`app/services/assessment_evaluator.py`)
- Calculates scores for MCQ/Aptitude rounds:
  - For each answered question:
    - If `selected_option.is_correct == True`: $+\text{marks}$
    - If `selected_option.is_correct == False`: $-\text{negative\_marks}$
    - If unattempted: $0$
  - Generates `assessment_results` row: `total_score`, `percentage`, `passed = (total_score >= passing_marks)`.
  - Computes percentile and ranks within the round cohort.

### 4.3 Coding Runner Abstraction (`app/services/coding_runner.py`)
- Evaluates code submissions against both public and hidden test cases.
- Implements time limit (e.g., 2000ms) and memory constraints.
- Sandboxed execution interface allowing future plug-in to Judge0, Docker isolated runner, or local subprocess execution.
- Computes `test_cases_passed / total_test_cases` and awards partial or full problem marks.

### 4.4 Multi-Round Progression & Shortlisting (`app/services/shortlist_service.py`)
- Manages the lifecycle of multi-round hiring competitions:
  - **Round 1 (Aptitude/MCQ):** Automated grading $\to$ Organizer cut-off filter $\to$ Shortlist generated.
  - **Round 2 (Coding):** Only students shortlisted from Round 1 can access Round 2 problems $\to$ Automated grading $\to$ Leaderboard $\to$ Round 2 Shortlist.
  - **Round 3 (Technical Interview):** 1-on-1 interview scheduled with Google Meet/Zoom link $\to$ Score & qualitative feedback submitted $\to$ Final Shortlist.
  - **Hiring Phase:** Organizer generates formal offer letter records (`hiring` table) $\to$ Student accepts or rejects in dashboard.

---

## 5. Security & Data Integrity

1. **Password Security:** Salted hashing with `bcrypt` (work factor 12). Plain passwords are never stored or logged.
2. **SQL Injection Prevention:** Strictly parameterized queries via SQLAlchemy 2.0 ORM expressions.
3. **CORS Policy:** Strict origin whitelisting configured for the React client (e.g. `http://localhost:3000`, `http://localhost:5173`).
4. **Organizer Verification Gate:** Organizers cannot publish events, view student contact info, or schedule interviews until their profile has been marked `APPROVED` by an Admin with a valid CIN verification.
5. **Exam Security:** During active assessments, answer keys (`is_correct`) and hidden test case answers are withheld from API responses sent to student clients.
