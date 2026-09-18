   
   tech stack:
   
                       ┌─────────────────────┐
                       │    REACT FRONTEND   │
                       │                     │
                       │ Student Dashboard   │
                       │ Organizer Dashboard │
                       │ Admin Dashboard     │
                       └──────────┬──────────┘
                                  │
                             HTTPS / REST
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │       FASTAPI       │
                       │                     │
                       │ Authentication      │
                       │        ↓            │
                       │ Authorization       │
                       │        ↓            │
                       │ Validation          │
                       │        ↓            │
                       │ Business Logic      │
                       │        ↓            │
                       │ Database Layer      │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │    SQL DATABASE     │
                       │                     │
                       │ Users               │
                       │ Organizer Profiles  │
                       │ Events              │
                       │ Participants        │
                       │ Scores              │
                       │ Achievements        │
                       │ Hiring              │
                       │ Blogs               │
                       │ Notifications       │
                       └─────────────────────┘


    data flow:

                         ┌───────────────┐
                         │   REGISTER    │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
           STUDENT           ORGANIZER            ADMIN
              │                  │                  │
              │               CIN +                 │
              │            Organization             │
              │                  │                  │
              │                  ▼                  │
              │               PENDING                │
              │                  │                  │
              │                  ▼                  │
              │            ADMIN VERIFY ◄────────────┘
              │                  │
              │            ┌─────┴─────┐
              │            ▼           ▼
              │         APPROVE      REJECT
              │            │
              │            ▼
              │        VERIFIED
              │
              ▼
        STUDENT LOGIN
              │
              ▼
       STUDENT DASHBOARD
              │
       ┌──────┼───────────────┐
       ▼      ▼               ▼
   Upcoming  My Events    Achievements
    Events
       │
       ▼
   EVENT DETAILS
       │
       ▼
    REGISTER
       │
       ▼
 EVENT REGISTRATION
       │
       ▼
    EVENT LIVE
       │
       ▼
     ROUND 1
       │
   ┌───┴────────────┐
   ▼                ▼
APTITUDE           MCQ
   │
   ▼
EVALUATION
   │
   ▼
SHORTLIST
   │
   ▼
     ROUND 2
       │
       ▼
    CODING
       │
       ▼
 CODE SUBMISSION
       │
       ▼
  EVALUATION
       │
       ▼
   SHORTLIST
       │
       ▼
     ROUND 3
       │
       ▼
 TECHNICAL INTERVIEW
       │
       ▼
 FINAL SHORTLIST
       │
       ▼
     HIRING

organizer side:

     ORGANIZER LOGIN
       │
       ▼
ORGANIZER DASHBOARD
       │
       ├── Create Event
       │      │
       │      ▼
       │   ADMIN APPROVAL
       │      │
       │      ▼
       │    EVENT LIVE
       │
       ├── Participants
       │      │
       │      ▼
       │   Student Profiles
       │      │
       │      ▼
       │   Achievements
       │
       ├── Rounds
       │      │
       │      ├── Create Aptitude
       │      ├── Create MCQ
       │      ├── Create Coding
       │      └── Create Interview
       │
       ├── Results
       │
       ├── Shortlisting
       │
       ├── Analytics
       │
       └── Hiring