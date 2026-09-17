DATABASE SCHEMA / ER-STYLE TABLE DESIGN
========================================


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


skills
--------------------------------
skill_id PK
name UNIQUE


student_skills
--------------------------------
student_id PK/FK → student_profiles.user_id
skill_id PK/FK → skills.skill_id
proficiency


events
--------------------------------
event_id PK
organization_id FK → organizations
created_by FK → users
title
description
event_type
event_mode
event_date
registration_deadline
location
max_participants
status
approved_by FK → users
approved_at
rejection_reason
created_at
updated_at


event_registrations
--------------------------------
registration_id PK
event_id FK → events
student_id FK → users
status
attendance_status
registered_at

UNIQUE(event_id, student_id)


event_rounds
--------------------------------
round_id PK
event_id FK → events
round_number
name
round_type
description
start_time
end_time
duration_minutes
total_marks
passing_marks
status
created_at
updated_at


assessments
--------------------------------
assessment_id PK
round_id FK → event_rounds
title
description
duration_minutes
total_marks
passing_marks
status
created_at
updated_at


questions
--------------------------------
question_id PK
assessment_id FK → assessments
question_text
question_type
marks
negative_marks
created_at


question_options
--------------------------------
option_id PK
question_id FK → questions
option_text
is_correct


answers
--------------------------------
answer_id PK
question_id FK → questions
assessment_id FK → assessments
student_id FK → users
selected_option_id FK → question_options
is_correct
marks_obtained
submitted_at

UNIQUE(question_id, student_id)


coding_problems
--------------------------------
problem_id PK
assessment_id FK → assessments
title
description
input_format
output_format
constraints
difficulty
created_at
updated_at


coding_test_cases
--------------------------------
test_case_id PK
problem_id FK → coding_problems
input_data
expected_output
marks
is_hidden


coding_submissions
--------------------------------
submission_id PK
problem_id FK → coding_problems
student_id FK → users
language
source_code
status
test_cases_passed
total_test_cases
score
submitted_at


assessment_results
--------------------------------
result_id PK
assessment_id FK → assessments
round_id FK → event_rounds
student_id FK → users
score
percentage
passed
rank
feedback
evaluated_at


round_shortlists
--------------------------------
shortlist_id PK
round_id FK → event_rounds
student_id FK → users
status
selected_by FK → users
selected_at
remarks


event_results
--------------------------------
result_id PK
event_id FK → events
student_id FK → users
overall_score
rank
feedback
evaluated_at


interviews
--------------------------------
interview_id PK
round_id FK → event_rounds
student_id FK → users
interviewer_id FK → users
scheduled_at
duration_minutes
meeting_url
status
score
feedback
created_at
updated_at


achievements
--------------------------------
achievement_id PK
name
description


student_achievements
--------------------------------
student_id FK → users
achievement_id FK → achievements
event_id FK → events
certificate_url
awarded_at


hiring
--------------------------------
hiring_id PK
student_id FK → users
organization_id FK → organizations
event_id FK → events
status
job_title
job_type
offered_at
accepted_at
rejected_at
created_at
updated_at


notifications
--------------------------------
notification_id PK
user_id FK → users
title
message
type
is_read
created_at


blogs
--------------------------------
blog_id PK
author_id FK → users
title
content
status
created_at
updated_at