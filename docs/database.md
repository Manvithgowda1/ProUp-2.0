database schema / ER-style table design

users
--------------------------------
user_id PK
email UNIQUE
password_hash
role
created_at
updated_at


organizations
--------------------------------
organization_id PK
name
cin UNIQUE
email
website
created_at


organizer_profiles
--------------------------------
user_id PK FK → users
organization_id FK → organizations
verification_status
verified_by FK → users
verified_at
rejection_reason


colleges
--------------------------------
college_id PK
name
location


student_profiles
--------------------------------
user_id PK FK → users
college_id FK → colleges
name
github_url
linkedin_url
resume_url
bio


events
--------------------------------
event_id PK
organization_id FK
created_by FK → users
title
description
event_date
registration_deadline
location
status
approved_by FK → users
approved_at
rejection_reason
created_at


event_registrations
--------------------------------
registration_id PK
event_id FK
student_id FK
status
attendance_status
registered_at


event_performances
--------------------------------
performance_id PK
registration_id FK
score
rank
feedback
evaluated_at


skills
--------------------------------
skill_id PK
name UNIQUE


student_skills
--------------------------------
student_id FK
skill_id FK
proficiency


achievements
--------------------------------
achievement_id PK
name
description


student_achievements
--------------------------------
student_id FK
achievement_id FK
event_id FK
awarded_at


hiring
--------------------------------
hiring_id PK
student_id FK
organization_id FK
event_id FK
status
created_at


notifications
--------------------------------
notification_id PK
user_id FK
title
message
type
is_read
created_at


blogs
--------------------------------
blog_id PK
author_id FK
title
content
status
created_at
updated_at