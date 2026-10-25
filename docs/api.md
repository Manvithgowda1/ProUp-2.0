# Proup REST API Specification (v1)

> **Platform:** Proup — Professional Upgrade  
> **Backend Framework:** FastAPI (Python 3.12+)  
> **Protocol:** HTTPS / REST  
> **Authentication:** Bearer Token (JWT - HS256)  
> **Base URL:** `/api/v1`  
> **Interactive Documentation:** Swagger UI at `/docs` | ReDoc at `/redoc` | OpenAPI JSON at `/api/v1/openapi.json`  

---

## 1. Authentication & Architecture Overview

### 1.1 Authentication Scheme
- **Mechanism:** OAuth2 with Bearer JWT tokens (`Authorization: Bearer <access_token>`).
- **Token Payload:**
  - `sub`: `user_id` (Integer serialized as string)
  - `email`: string
  - `role`: `student` | `organizer` | `admin`
  - `org_id`: (optional) Integer (for organizers)
  - `exp`: expiration timestamp (60 minutes for access token, 7 days for refresh token)
  - `type`: `"access"` | `"refresh"`
- **Role-Based Access Control (RBAC):**
  - **Public:** Accessible without token (e.g., login, register, public event listings, health check).
  - **Student:** Registered users with `role = "student"`.
  - **Organizer:** Registered users with `role = "organizer"` and `verification_status = "APPROVED"`.
  - **Admin:** Elevated users with `role = "admin"`.

### 1.2 Common HTTP Status Codes
| Code | Meaning | Description |
| :--- | :--- | :--- |
| `200 OK` | Success | Request succeeded with data payload. |
| `201 Created` | Created | Resource successfully created. |
| `400 Bad Request` | Client Error | Malformed request or business validation failed. |
| `401 Unauthorized` | Auth Error | Missing, expired, or invalid JWT token. |
| `403 Forbidden` | Permission Denied | Insufficient permissions for user role or unapproved organizer. |
| `404 Not Found` | Not Found | Requested entity does not exist. |
| `409 Conflict` | Conflict | Duplicate entry (e.g., email already registered, already registered for event). |
| `422 Unprocessable` | Validation Error | Pydantic schema validation error. |
| `500 Server Error` | Server Error | Internal unexpected error. |

### 1.3 Standard Response Envelope
All API endpoints return data wrapped in `APIResponse[T]`:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

Error responses from FastAPI exceptions:
```json
{
  "detail": "Descriptive error message"
}
```

---

## 2. Implemented Backend Endpoints

---

### Domain 1: Authentication (`/api/v1/auth`)

#### 1.1 Student Registration
- **POST** `/api/v1/auth/register/student`
- **Access:** Public
- **Request Body (`StudentRegisterRequest`):**
```json
{
  "email": "student@nie.ac.in",
  "password": "StrongPassword123!",
  "name": "Manvith Gowda",
  "college_id": 1,
  "github_url": "https://github.com/manvithgowda",
  "linkedin_url": "https://linkedin.com/in/manvithgowda",
  "bio": "Backend engineer & systems enthusiast",
  "skills": [
    {"skill_id": 1, "proficiency": "ADVANCED"},
    {"skill_id": 2, "proficiency": "ADVANCED"}
  ]
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "message": "Student registered successfully",
  "data": {
    "user_id": 101,
    "email": "student@nie.ac.in",
    "role": "student",
    "verification_status": null,
    "organization_id": null
  }
}
```

#### 1.2 Organizer Registration
- **POST** `/api/v1/auth/register/organizer`
- **Access:** Public
- **Description:** Registers an organizer account with company details and CIN for admin verification. Defaults to `PENDING` verification status.
- **Request Body (`OrganizerRegisterRequest`):**
```json
{
  "email": "recruiter@deepmind.com",
  "password": "SecurePassword123!",
  "organization": {
    "name": "Google DeepMind Labs",
    "cin": "U72900KA2021PTC148900",
    "email": "careers@deepmind.com",
    "website": "https://deepmind.google"
  }
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "message": "Organizer registration submitted for admin approval",
  "data": {
    "user_id": 202,
    "email": "recruiter@deepmind.com",
    "role": "organizer",
    "verification_status": "PENDING",
    "organization_id": 15
  }
}
```

#### 1.3 User Login
- **POST** `/api/v1/auth/login`
- **Access:** Public
- **Request Body (`LoginRequest`):**
```json
{
  "email": "student@nie.ac.in",
  "password": "StrongPassword123!"
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "user_id": 101,
      "email": "student@nie.ac.in",
      "role": "student",
      "verification_status": null,
      "organization_id": null
    }
  }
}
```

#### 1.4 Get Current User Profile (`/me`)
- **GET** `/api/v1/auth/me`
- **Access:** Authenticated (Any role)
- **Response (200 OK):** Current user object with user_id, email, role, verification_status, and organization_id.

---

### Domain 2: Students (`/api/v1/students`)

#### 2.1 Get Current Student Profile
- **GET** `/api/v1/students/me/profile`
- **Access:** Student (`require_role(["student"])`)
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "user_id": 101,
    "name": "Manvith Gowda",
    "email": "student@nie.ac.in",
    "college": {
      "college_id": 1,
      "name": "National Institute of Engineering",
      "location": "Mysuru"
    },
    "github_url": "https://github.com/manvithgowda",
    "linkedin_url": "https://linkedin.com/in/manvithgowda",
    "resume_url": null,
    "bio": "Backend engineer & systems enthusiast",
    "skills": [
      {"skill_id": 1, "name": "Python", "proficiency": "ADVANCED"},
      {"skill_id": 2, "name": "FastAPI", "proficiency": "ADVANCED"}
    ]
  }
}
```

#### 2.2 Update Student Profile
- **PUT** `/api/v1/students/me/profile`
- **Access:** Student
- **Request Body (`StudentProfileUpdate`):**
```json
{
  "name": "Manvith Gowda",
  "college_id": 1,
  "github_url": "https://github.com/manvithgowda",
  "linkedin_url": "https://linkedin.com/in/manvithgowda",
  "resume_url": "https://storage.proup.io/resumes/101.pdf",
  "bio": "Updated bio text"
}
```
- **Response (200 OK):** Refreshed `StudentProfileResponse`.

#### 2.3 Manage Student Skills
- **POST** `/api/v1/students/me/skills`
  - **Access:** Student
  - **Request Body (`AddSkillRequest`):** `{"skill_id": 3, "proficiency": "INTERMEDIATE"}`
  - **Response (200 OK):** `{"success": true, "message": "Skill added successfully", "data": {"skill_id": 3}}`
- **DELETE** `/api/v1/students/me/skills/{skill_id}`
  - **Access:** Student
  - **Response (200 OK):** `{"success": true, "message": "Skill removed successfully", "data": {"skill_id": 3}}`

#### 2.4 Get Student Achievements
- **GET** `/api/v1/students/me/achievements`
- **Access:** Student
- **Description:** Returns the student's verified achievements and participation credentials (PRD Section 5.2).

#### 2.5 Get Student Event Registrations ("My Events")
- **GET** `/api/v1/students/me/registrations`
- **Access:** Student
- **Description:** Returns all events the student has registered for.

---

### Domain 3: Events (`/api/v1/events`)

#### 3.1 Public Event Discovery
- **GET** `/api/v1/events`
- **Access:** Public
- **Query Parameters:**
  - `status`: string (default `"LIVE"`, or `"ALL"`, `"DRAFT"`, `"APPROVED"`)
  - `event_type`: string (optional: `"HIRING_CHALLENGE"`, `"HACKATHON"`, `"COMPETITION"`, `"WORKSHOP"`)
  - `search`: string (keyword search matching title or description)
  - `page`: integer (default `1`)
  - `limit`: integer (default `20`, max `100`)
- **Response (200 OK):** Paginated event objects with nested organization details and `rounds_count`.

#### 3.2 Skill-Based Event Recommendations
- **GET** `/api/v1/events/recommendations`
- **Access:** Student
- **Description:** Runs the recommendation engine based on student skills and event keywords, returning events ranked by `match_score` (0.0 to 100.0).
- **Response (200 OK):** List of `EventRecommendation` objects.

#### 3.3 Get Event Details
- **GET** `/api/v1/events/{event_id}`
- **Access:** Public
- **Response (200 OK):** Single `EventResponse` with organizer brief and rounds count.

#### 3.4 Create Event
- **POST** `/api/v1/events`
- **Access:** Verified Organizer / Admin (`require_verified_organizer`)
- **Status:** `201 Created`
- **Request Body (`EventCreate`):**
```json
{
  "title": "National Systems & Backend Hiring Challenge 2026",
  "description": "High-velocity 3-stage competition for top engineers.",
  "event_type": "HIRING_CHALLENGE",
  "event_mode": "ONLINE",
  "event_date": "2026-11-15T09:00:00Z",
  "registration_deadline": "2026-11-10T23:59:59Z",
  "location": "Remote",
  "max_participants": 500
}
```
- **Response (201 Created):** `{"success": true, "message": "Event created in DRAFT status", "data": {"event_id": 1, "status": "DRAFT"}}`

#### 3.5 Register for Event
- **POST** `/api/v1/events/{event_id}/register`
- **Access:** Student
- **Response (200 OK):** `{"success": true, "message": "Successfully registered for event", "data": {"event_id": 1}}`

#### 3.6 Update Event
- **PUT** `/api/v1/events/{event_id}`
- **Access:** Verified Organizer (Creator) / Admin
- **Request Body (`EventUpdate`):** `{"title": "Updated Title", "max_participants": 600}`
- **Response (200 OK):** `{"success": true, "message": "Event updated successfully", "data": {"event_id": 1}}`

#### 3.7 Get Event Rounds
- **GET** `/api/v1/events/{event_id}/rounds`
- **Access:** Public
- **Response (200 OK):** List of competition rounds with duration, marks, and round type.

---

### Domain 4: Assessments (`/api/v1/assessments`)

#### 4.1 Get Assessment Questions
- **GET** `/api/v1/assessments/{assessment_id}/questions`
- **Access:** Authenticated (Any role)
- **Note:** `is_correct` field is automatically concealed (`null`) when requested by students taking the test.
- **Response (200 OK):** List of `QuestionResponse` objects with question options.

#### 4.2 Add Question to Assessment
- **POST** `/api/v1/assessments/{assessment_id}/questions`
- **Access:** Verified Organizer / Admin
- **Status:** `201 Created`
- **Request Body (`QuestionCreate`):**
```json
{
  "question_text": "What is the time complexity of searching in a balanced BST?",
  "question_type": "MCQ",
  "marks": 2.0,
  "negative_marks": 0.5,
  "options": [
    {"option_text": "O(1)", "is_correct": false},
    {"option_text": "O(log n)", "is_correct": true},
    {"option_text": "O(n)", "is_correct": false},
    {"option_text": "O(n log n)", "is_correct": false}
  ]
}
```
- **Response (201 Created):** `{"success": true, "message": "Question created successfully", "data": {"question_id": 1}}`

#### 4.3 Submit Assessment Answers & Automated Grading
- **POST** `/api/v1/assessments/{assessment_id}/submit`
- **Access:** Student
- **Request Body (`AssessmentSubmitRequest`):**
```json
{
  "submissions": [
    {"question_id": 1, "selected_option_id": 2},
    {"question_id": 2, "selected_option_id": 7}
  ]
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Assessment evaluated successfully",
  "data": {
    "result_id": 1,
    "assessment_id": 1,
    "student_id": 101,
    "score": 85.5,
    "total_marks": 100.0,
    "percentage": 85.5,
    "passed": true,
    "rank": null
  }
}
```

---

### Domain 5: Coding Arena (`/api/v1/coding`)

#### 5.1 Get Coding Problem
- **GET** `/api/v1/coding/problems/{problem_id}`
- **Access:** Authenticated (Any role)
- **Note:** Hidden test cases (`is_hidden = true`) are filtered out for student users.
- **Response (200 OK):** `CodingProblemResponse` with description, formats, constraints, and public test cases.

#### 5.2 Add Test Case
- **POST** `/api/v1/coding/problems/{problem_id}/test-cases`
- **Access:** Verified Organizer / Admin
- **Status:** `201 Created`
- **Request Body (`TestCaseCreate`):**
```json
{
  "input_data": "4\n2 7 11 15\n9",
  "expected_output": "0 1",
  "marks": 10.0,
  "is_hidden": true
}
```
- **Response (201 Created):** `{"success": true, "message": "Test case created", "data": {"test_case_id": 1}}`

#### 5.3 Submit Code for Execution
- **POST** `/api/v1/coding/problems/{problem_id}/submit`
- **Access:** Student
- **Request Body (`CodeSubmissionRequest`):**
```json
{
  "language": "python",
  "source_code": "def solve():\n    return 0"
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Code evaluated",
  "data": {
    "submission_id": 1,
    "problem_id": 1,
    "language": "python",
    "status": "ACCEPTED",
    "test_cases_passed": 3,
    "total_test_cases": 3,
    "score": 100.0
  }
}
```

---

### Domain 6: Hiring & Job Offers (`/api/v1/hiring`)

#### 6.1 Extend Job Offer
- **POST** `/api/v1/hiring/offers`
- **Access:** Verified Organizer / Admin
- **Status:** `201 Created`
- **Request Body (`OfferCreate`):**
```json
{
  "student_id": 101,
  "event_id": 1,
  "job_title": "Junior Backend Engineer",
  "job_type": "FULL_TIME"
}
```
- **Response (201 Created):** `{"success": true, "message": "Job offer extended successfully", "data": {"hiring_id": 1}}`

#### 6.2 Get Student's Received Offers
- **GET** `/api/v1/hiring/my-offers`
- **Access:** Student
- **Response (200 OK):** List of `OfferResponse` objects.

#### 6.3 Respond to Offer (Accept / Reject)
- **PATCH** `/api/v1/hiring/offers/{hiring_id}/respond`
- **Access:** Student
- **Request Body (`OfferRespond`):** `{"status": "ACCEPTED"}` *(or `"REJECTED"`)*
- **Response (200 OK):** `{"success": true, "message": "Offer accepted successfully", "data": {"hiring_id": 1}}`

---

### Domain 7: Admin Oversight & Analytics (`/api/v1/admin`)

#### 7.1 View Pending Organizers
- **GET** `/api/v1/admin/organizers/pending`
- **Access:** Admin
- **Response (200 OK):** List of pending organizers with organization details and CIN.

#### 7.2 Verify Organizer
- **POST** `/api/v1/admin/organizers/{user_id}/verify`
- **Access:** Admin
- **Request Body (`OrganizerVerifyRequest`):** `{"status": "APPROVED", "rejection_reason": null}` *(or `"REJECTED"`)*
- **Response (200 OK):** `{"success": true, "message": "Organizer verification set to APPROVED", "data": {"user_id": 202}}`

#### 7.3 Moderate Event
- **POST** `/api/v1/admin/events/{event_id}/moderate`
- **Access:** Admin
- **Request Body (`EventModerateRequest`):** `{"status": "APPROVED", "rejection_reason": null}` *(or `"REJECTED"`)*
- **Response (200 OK):** `{"success": true, "message": "Event moderated to LIVE", "data": {"event_id": 1}}`

#### 7.4 Platform Analytics
- **GET** `/api/v1/admin/analytics`
- **Access:** Admin
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "total_students": 1,
    "total_organizers": 1,
    "total_events": 1,
    "total_registrations": 1,
    "total_shortlisted": 0,
    "total_hired": 1,
    "active_events": 1
  }
}
```

---

## 3. Seeded Accounts for Testing

Run `python -m app.seed` from the `server` directory to initialize:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@proup.io` | `Admin@123` |
| **Organizer** | `recruiter@deepmind.com` | `Recruiter@123` |
| **Student** | `student@nie.ac.in` | `Student@123` |

---

## 4. Planned Roadmap Endpoints (Subsequent Milestones)

The database schema and models in `app/models/` support the following endpoints planned for upcoming iterations:
- **Rounds Management:** `/api/v1/events/{id}/rounds`, `/api/v1/rounds/{id}/shortlist`
- **Interviews:** `/api/v1/rounds/{id}/interviews`, `/api/v1/interviews/{id}`
- **Achievements & Certificates:** `/api/v1/events/{id}/award-achievements`, `/api/v1/students/{id}/achievements`
- **Notifications:** `/api/v1/notifications`, `/api/v1/notifications/{id}/read`
- **Blogs:** `/api/v1/blogs`
