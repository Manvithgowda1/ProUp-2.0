# Proup REST API Specification (v1)

> **Platform:** Proup — Professional Upgrade  
> **Backend Framework:** FastAPI (Python 3.12+)  
> **Protocol:** HTTPS / REST  
> **Authentication:** Bearer Token (JWT - JSON Web Tokens)  
> **Base URL:** `/api/v1`

---

## 1. Authentication & Architecture Overview

### 1.1 Authentication Scheme
- **Mechanism:** OAuth2 with Bearer JWT tokens (`Authorization: Bearer <access_token>`).
- **Token Payload:**
  - `sub`: `user_id` (UUID / Integer)
  - `email`: string
  - `role`: `student` | `organizer` | `admin`
  - `org_id`: (optional) Integer (for organizers)
  - `exp`: expiration timestamp (e.g., 30 minutes for access token, 7 days for refresh token)
- **Role-Based Access Control (RBAC):**
  - **Public:** Accessible without token (e.g., login, register, public event listings).
  - **Student:** Registered users with `role = "student"`.
  - **Organizer:** Registered users with `role = "organizer"` and `verification_status = "APPROVED"`.
  - **Admin:** Elevated users with `role = "admin"`.

### 1.2 Common HTTP Status Codes
| Code | Meaning | Description |
| :--- | :--- | :--- |
| `200 OK` | Success | Request succeeded with data payload. |
| `201 Created` | Created | Resource successfully created. |
| `204 No Content` | No Content | Action succeeded with no payload returned. |
| `400 Bad Request` | Client Error | Malformed request, business logic validation failed. |
| `401 Unauthorized` | Auth Error | Missing, expired, or invalid JWT token. |
| `403 Forbidden` | Permission Denied | Insufficient permissions for user role (e.g., student trying to create event). |
| `404 Not Found` | Not Found | Requested entity does not exist. |
| `409 Conflict` | Conflict | Duplicate entry (e.g., email already registered, already registered for event). |
| `422 Unprocessable` | Validation Error | Pydantic schema validation error. |
| `500 Server Error` | Server Error | Internal unexpected error. |

### 1.3 Standard Response Format
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```
Error Response:
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested event does not exist",
    "details": null
  }
}
```

---

## 2. API Endpoints by Domain

---

### Domain 1: Authentication & Account Management (`/api/v1/auth`)

#### 1.1 Student Registration
- **POST** `/auth/register/student`
- **Access:** Public
- **Request Body:**
```json
{
  "email": "student@college.edu",
  "password": "StrongPassword123!",
  "name": "Jane Doe",
  "college_id": 1,
  "github_url": "https://github.com/janedoe",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "bio": "Passionate backend engineer and competitive programmer",
  "skills": [
    {"skill_id": 1, "proficiency": "ADVANCED"},
    {"skill_id": 4, "proficiency": "INTERMEDIATE"}
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
    "email": "student@college.edu",
    "role": "student",
    "created_at": "2026-10-11T12:00:00Z"
  }
}
```

#### 1.2 Organizer Registration
- **POST** `/auth/register/organizer`
- **Access:** Public
- **Description:** Registers an organizer account along with company/organization details and CIN for admin verification.
- **Request Body:**
```json
{
  "email": "hr@techcorp.com",
  "password": "SecurePassword123!",
  "organization": {
    "name": "TechCorp Innovations Pvt Ltd",
    "cin": "U72200KA2020PTC123456",
    "email": "contact@techcorp.com",
    "website": "https://techcorp.com"
  }
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "message": "Organizer registration submitted for admin verification",
  "data": {
    "user_id": 202,
    "email": "hr@techcorp.com",
    "role": "organizer",
    "verification_status": "PENDING",
    "organization_id": 15
  }
}
```

#### 1.3 User Login
- **POST** `/auth/login`
- **Access:** Public
- **Request Body:**
```json
{
  "email": "hr@techcorp.com",
  "password": "SecurePassword123!"
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "user_id": 202,
      "email": "hr@techcorp.com",
      "role": "organizer",
      "verification_status": "APPROVED",
      "organization_id": 15
    }
  }
}
```

#### 1.4 Refresh Token
- **POST** `/auth/refresh`
- **Access:** Public (Requires valid Refresh Token)
- **Request Body:** `{"refresh_token": "..."}`
- **Response (200 OK):** `{"access_token": "...", "expires_in": 1800}`

#### 1.5 Get Current User (`Me`)
- **GET** `/auth/me`
- **Access:** Authenticated (Any role)
- **Response (200 OK):** Current user object with associated profile details.

---

### Domain 2: Student Profiles & Skills (`/api/v1/students`, `/api/v1/skills`, `/api/v1/colleges`)

#### 2.1 Get Current Student Profile
- **GET** `/students/me/profile`
- **Access:** Student
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": 101,
    "name": "Jane Doe",
    "email": "student@college.edu",
    "college": {
      "college_id": 1,
      "name": "National Institute of Engineering",
      "location": "Mysuru"
    },
    "github_url": "https://github.com/janedoe",
    "linkedin_url": "https://linkedin.com/in/janedoe",
    "resume_url": "https://storage.proup.io/resumes/101.pdf",
    "bio": "Backend engineer & competitive programmer",
    "skills": [
      {"skill_id": 1, "name": "Python", "proficiency": "ADVANCED"},
      {"skill_id": 2, "name": "FastAPI", "proficiency": "ADVANCED"},
      {"skill_id": 5, "name": "PostgreSQL", "proficiency": "INTERMEDIATE"}
    ]
  }
}
```

#### 2.2 Update Student Profile
- **PUT** `/students/me/profile`
- **Access:** Student
- **Request Body:**
```json
{
  "name": "Jane Doe",
  "college_id": 1,
  "github_url": "https://github.com/janedoe",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "resume_url": "https://storage.proup.io/resumes/101.pdf",
  "bio": "Updated bio text"
}
```

#### 2.3 Manage Student Skills
- **POST** `/students/me/skills`
  - **Request Body:** `{"skill_id": 3, "proficiency": "BEGINNER" | "INTERMEDIATE" | "ADVANCED"}`
- **DELETE** `/students/me/skills/{skill_id}`
- **GET** `/skills` (Public master list with search: `?query=python`)
- **GET** `/colleges` (Public master list with search: `?query=institute`)

#### 2.4 Public Student Profile (with verified achievements)
- **GET** `/students/{student_id}/profile`
- **Access:** Authenticated (Student, Organizer, Admin)
- **Response (200 OK):** Returns student bio, skills, verified achievements, and event participation track record.

---

### Domain 3: Events Management (`/api/v1/events`)

#### 3.1 Public Event Discovery
- **GET** `/events`
- **Access:** Public
- **Query Parameters:**
  - `page`: integer (default 1)
  - `limit`: integer (default 20)
  - `status`: string (default "LIVE", or "UPCOMING")
  - `event_type`: "HACKATHON" | "COMPETITION" | "WORKSHOP" | "HIRING_CHALLENGE"
  - `event_mode`: "ONLINE" | "OFFLINE" | "HYBRID"
  - `search`: string (title / description keyword)
  - `organization_id`: integer
- **Response (200 OK):** Paginated event objects with organizer details.

#### 3.2 Get Event Details
- **GET** `/events/{event_id}`
- **Access:** Public
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "event_id": 10,
    "title": "National Backend Hackathon 2026",
    "description": "3-round high-stakes coding & backend engineering event",
    "event_type": "HIRING_CHALLENGE",
    "event_mode": "ONLINE",
    "event_date": "2026-11-15T09:00:00Z",
    "registration_deadline": "2026-11-10T23:59:59Z",
    "location": "Virtual / Remote",
    "max_participants": 500,
    "current_participants": 142,
    "status": "LIVE",
    "organization": {
      "organization_id": 15,
      "name": "TechCorp Innovations Pvt Ltd",
      "website": "https://techcorp.com"
    },
    "rounds_count": 3
  }
}
```

#### 3.3 Skill-Based Event Recommendations
- **GET** `/events/recommendations`
- **Access:** Student
- **Description:** Ranks upcoming events based on Jaccard/weighted overlap between student's registered skills and event tags/rounds.
- **Response (200 OK):** List of recommended events with match score percentage.

#### 3.4 Create Event (Organizer)
- **POST** `/events`
- **Access:** Organizer (Verified only)
- **Request Body:**
```json
{
  "title": "Cloud Architect Hiring Sprint",
  "description": "Evaluate candidates across Aptitude, Coding, and System Design Interview.",
  "event_type": "HIRING_CHALLENGE",
  "event_mode": "ONLINE",
  "event_date": "2026-12-01T10:00:00Z",
  "registration_deadline": "2026-11-25T18:00:00Z",
  "location": "Online",
  "max_participants": 200
}
```
- **Response (201 Created):** Created event object with `status = "DRAFT"`.

#### 3.5 Submit Event for Admin Approval
- **POST** `/events/{event_id}/submit`
- **Access:** Organizer (Event owner)
- **Description:** Transitions event status from `DRAFT` to `PENDING_APPROVAL`.

#### 3.6 Organizer's Events List
- **GET** `/organizers/me/events`
- **Access:** Organizer
- **Query Parameters:** `?status=ALL|DRAFT|PENDING_APPROVAL|APPROVED|LIVE|COMPLETED`

---

### Domain 4: Event Registrations & Participants (`/api/v1/registrations`)

#### 4.1 Register for Event
- **POST** `/events/{event_id}/register`
- **Access:** Student
- **Response (201 Created):**
```json
{
  "success": true,
  "message": "Registered successfully for event",
  "data": {
    "registration_id": 55,
    "event_id": 10,
    "student_id": 101,
    "status": "REGISTERED",
    "registered_at": "2026-10-11T14:30:00Z"
  }
}
```

#### 4.2 Cancel Event Registration
- **DELETE** `/events/{event_id}/register`
- **Access:** Student
- **Response (200 OK):** Registration marked as `CANCELLED`.

#### 4.3 Student's Registered Events ("My Events")
- **GET** `/students/me/registrations`
- **Access:** Student
- **Query Parameters:** `?status=UPCOMING|ONGOING|COMPLETED`

#### 4.4 View Event Participants
- **GET** `/events/{event_id}/participants`
- **Access:** Organizer (Event owner), Admin
- **Query Parameters:** `?page=1&limit=50&attendance_status=ALL|PRESENT|ABSENT`
- **Response (200 OK):** Participant list with student profiles, scores, and status.

#### 4.5 Mark Attendance
- **PATCH** `/events/{event_id}/participants/{student_id}/attendance`
- **Access:** Organizer
- **Request Body:** `{"attendance_status": "PRESENT" | "ABSENT"}`

---

### Domain 5: Rounds & Assessments (`/api/v1/rounds`, `/api/v1/assessments`)

#### 5.1 List Event Rounds
- **GET** `/events/{event_id}/rounds`
- **Access:** Authenticated (Student registered / Organizer / Admin)
- **Response (200 OK):** List of rounds (Round 1: Aptitude/MCQ, Round 2: Coding, Round 3: Interview).

#### 5.2 Create Event Round
- **POST** `/events/{event_id}/rounds`
- **Access:** Organizer
- **Request Body:**
```json
{
  "round_number": 1,
  "name": "General Aptitude & CS Fundamentals",
  "round_type": "APTITUDE",
  "description": "60 questions covering quantitative ability and CS basics",
  "start_time": "2026-11-15T10:00:00Z",
  "end_time": "2026-11-15T11:00:00Z",
  "duration_minutes": 60,
  "total_marks": 100,
  "passing_marks": 60
}
```

#### 5.3 Configure Assessment for Round
- **POST** `/rounds/{round_id}/assessments`
- **Access:** Organizer
- **Request Body:**
```json
{
  "title": "Aptitude Assessment 2026",
  "description": "Timed evaluation test",
  "duration_minutes": 60,
  "total_marks": 100,
  "passing_marks": 60
}
```

---

### Domain 6: Question Bank & MCQ Submissions (`/api/v1/assessments/{id}/questions`, `/answers`)

#### 6.1 Add Questions (MCQ / Aptitude)
- **POST** `/assessments/{assessment_id}/questions`
- **Access:** Organizer
- **Request Body:**
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

#### 6.2 Get Assessment Questions (Student View)
- **GET** `/assessments/{assessment_id}/questions`
- **Access:** Student (Registered & shortlisted for this round)
- **Note:** `is_correct` field is stripped from all options for students.

#### 6.3 Submit Assessment Answers
- **POST** `/assessments/{assessment_id}/submit`
- **Access:** Student
- **Request Body:**
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
  "message": "Assessment submitted and evaluated",
  "data": {
    "score": 85.5,
    "total_marks": 100,
    "percentage": 85.5,
    "passed": true
  }
}
```

---

### Domain 7: Coding Arena & Automated Evaluation (`/api/v1/coding`)

#### 7.1 Create Coding Problem
- **POST** `/assessments/{assessment_id}/coding-problems`
- **Access:** Organizer
- **Request Body:**
```json
{
  "title": "Two Sum Variations",
  "description": "Given an array of integers nums and an integer target...",
  "input_format": "First line N, next line N space-separated integers, third line target",
  "output_format": "Indices i and j",
  "constraints": "2 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9",
  "difficulty": "MEDIUM"
}
```

#### 7.2 Add Test Cases to Coding Problem
- **POST** `/coding-problems/{problem_id}/test-cases`
- **Access:** Organizer
- **Request Body:**
```json
{
  "input_data": "4\n2 7 11 15\n9",
  "expected_output": "0 1",
  "marks": 10.0,
  "is_hidden": false
}
```

#### 7.3 Submit Code for Execution
- **POST** `/coding-problems/{problem_id}/submit`
- **Access:** Student
- **Request Body:**
```json
{
  "language": "python",
  "source_code": "def solve():\n    n = int(input())\n    nums = list(map(int, input().split()))\n    target = int(input())\n    ..."
}
```
- **Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "submission_id": 312,
    "status": "ACCEPTED",
    "test_cases_passed": 5,
    "total_test_cases": 5,
    "score": 50.0,
    "runtime_ms": 42
  }
}
```

---

### Domain 8: Round Shortlisting & Event Results (`/api/v1/rounds/{round_id}/shortlist`, `/events/{id}/results`)

#### 8.1 View Round Leaderboard / Assessment Results
- **GET** `/rounds/{round_id}/results`
- **Access:** Organizer, Admin
- **Response (200 OK):** Ranked list of students based on assessment/coding score.

#### 8.2 Shortlist Students for Next Round
- **POST** `/rounds/{round_id}/shortlist`
- **Access:** Organizer
- **Request Body:**
```json
{
  "student_ids": [101, 104, 108],
  "status": "SHORTLISTED",
  "remarks": "Qualified Round 1 Aptitude with top 10 percentile"
}
```

#### 8.3 Get Round Shortlist
- **GET** `/rounds/{round_id}/shortlist`
- **Access:** Authenticated (Student can check own status; Organizer/Admin can view all)

#### 8.4 Finalize Event Results
- **POST** `/events/{event_id}/finalize-results`
- **Access:** Organizer
- **Request Body:**
```json
{
  "results": [
    {"student_id": 101, "overall_score": 94.5, "rank": 1, "feedback": "Exceptional backend problem solving"},
    {"student_id": 104, "overall_score": 91.0, "rank": 2, "feedback": "Strong algorithmic performance"}
  ]
}
```

---

### Domain 9: Interviews (`/api/v1/interviews`)

#### 9.1 Schedule Interview
- **POST** `/rounds/{round_id}/interviews`
- **Access:** Organizer
- **Request Body:**
```json
{
  "student_id": 101,
  "interviewer_id": 202,
  "scheduled_at": "2026-11-20T14:00:00Z",
  "duration_minutes": 45,
  "meeting_url": "https://meet.google.com/abc-defg-hij"
}
```

#### 9.2 Update Interview Feedback & Score
- **PATCH** `/interviews/{interview_id}`
- **Access:** Organizer / Interviewer
- **Request Body:**
```json
{
  "status": "COMPLETED",
  "score": 90.0,
  "feedback": "Great understanding of distributed systems and database indexing."
}
```

#### 9.3 Get Student's Interviews
- **GET** `/students/me/interviews`
- **Access:** Student

---

### Domain 10: Achievements & Certificates (`/api/v1/achievements`)

#### 10.1 Award Achievement & Certificate
- **POST** `/events/{event_id}/award-achievements`
- **Access:** Organizer, Admin
- **Request Body:**
```json
{
  "student_id": 101,
  "achievement_id": 1,
  "certificate_url": "https://storage.proup.io/certificates/cert-101-event-10.pdf"
}
```

#### 10.2 Get Student Achievements
- **GET** `/students/{student_id}/achievements`
- **Access:** Public / Authenticated
- **Response (200 OK):** List of verified achievements, event names, issuing organizations, and certificate URLs.

---

### Domain 11: Hiring & Job Offers (`/api/v1/hiring`)

#### 11.1 Extend Job Offer
- **POST** `/hiring/offers`
- **Access:** Organizer
- **Request Body:**
```json
{
  "student_id": 101,
  "event_id": 10,
  "job_title": "Junior Backend Engineer",
  "job_type": "FULL_TIME",
  "details": "Salary: ₹12 LPA, Location: Bengaluru"
}
```

#### 11.2 Student View Offers
- **GET** `/students/me/offers`
- **Access:** Student

#### 11.3 Student Respond to Offer
- **PATCH** `/students/me/offers/{hiring_id}`
- **Access:** Student
- **Request Body:**
```json
{
  "status": "ACCEPTED" // or "REJECTED"
}
```

---

### Domain 12: Admin Moderation & Platform Analytics (`/api/v1/admin`)

#### 12.1 Pending Organizers Verification
- **GET** `/admin/organizers/pending`
- **Access:** Admin
- **Response (200 OK):** List of pending organizers with CIN and organization info.

#### 12.2 Verify Organizer (Approve / Reject)
- **POST** `/admin/organizers/{user_id}/verify`
- **Access:** Admin
- **Request Body:**
```json
{
  "status": "APPROVED", // or "REJECTED"
  "rejection_reason": null
}
```

#### 12.3 Pending Events Moderation
- **GET** `/admin/events/pending`
- **Access:** Admin

#### 12.4 Moderate Event (Approve / Reject)
- **POST** `/admin/events/{event_id}/moderate`
- **Access:** Admin
- **Request Body:**
```json
{
  "status": "APPROVED", // or "REJECTED"
  "rejection_reason": null
}
```

#### 12.5 Platform Analytics
- **GET** `/admin/analytics`
- **Access:** Admin
- **Response (200 OK):**
```json
{
  "total_students": 1250,
  "total_organizers": 45,
  "total_events": 88,
  "total_registrations": 4320,
  "total_shortlisted": 620,
  "total_hired": 94,
  "active_events": 12
}
```

---

### Domain 13: Notifications & Blogs (`/api/v1/notifications`, `/api/v1/blogs`)

#### 13.1 Notifications
- **GET** `/notifications` (Get user's notifications)
- **PATCH** `/notifications/{id}/read` (Mark notification as read)
- **PATCH** `/notifications/read-all` (Mark all as read)

#### 13.2 Blogs
- **GET** `/blogs` (Public list of published blogs)
- **GET** `/blogs/{id}` (Blog detail)
- **POST** `/blogs` (Create blog post - Admin / Organizer / Author)
- **PUT** `/blogs/{id}` (Update blog)
