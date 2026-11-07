-- Proup Platform Seed Data Script
-- Inserts initial Master Data, Admin, Organizer, Student, and Sample Event

BEGIN;

-- 1. Seed Colleges
INSERT INTO colleges (name, location) VALUES 
('National Institute of Engineering', 'Mysuru'),
('PES University', 'Bengaluru'),
('BMS College of Engineering', 'Bengaluru')
ON CONFLICT DO NOTHING;

-- 2. Seed Skills Master Data
INSERT INTO skills (name) VALUES 
('Python'),
('FastAPI'),
('PostgreSQL'),
('React'),
('TypeScript'),
('Docker'),
('Data Structures & Algorithms')
ON CONFLICT DO NOTHING;

-- 3. Seed Admin User (Password: Admin@123)
INSERT INTO users (user_id, email, password_hash, role, created_at, updated_at) VALUES 
(1, 'admin@proup.io', '$2b$12$UIVgXsD6XLnRfTMpGC1PtuF2quk1VhAIVVvVmkN2TJ7nlSDYZmOWW', 'admin', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

-- 4. Seed Organization
INSERT INTO organizations (organization_id, name, cin, email, website, created_at) VALUES 
(1, 'Google DeepMind Labs', 'U72900KA2021PTC148900', 'careers@deepmind.com', 'https://deepmind.google', NOW())
ON CONFLICT (cin) DO NOTHING;

-- 5. Seed Organizer User (Password: Recruiter@123)
INSERT INTO users (user_id, email, password_hash, role, created_at, updated_at) VALUES 
(2, 'recruiter@deepmind.com', '$2b$12$WamJupjEcNAIE6EpMWY6s.HXYxEbszCYVeu2uuLjcsKuqHkaRNv/m', 'organizer', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO organizer_profiles (user_id, organization_id, verification_status, verified_by, verified_at) VALUES 
(2, 1, 'APPROVED', 1, NOW())
ON CONFLICT (user_id) DO NOTHING;

-- 6. Seed Student User (Password: Student@123)
INSERT INTO users (user_id, email, password_hash, role, created_at, updated_at) VALUES 
(3, 'student@nie.ac.in', '$2b$12$2QQ6gkWVbvwrGkEXkHm4vOnNuH.r8JYKiZbZgaB0BTVIMumgVzRUO', 'student', NOW(), NOW())
ON CONFLICT (email) DO NOTHING;

INSERT INTO student_profiles (user_id, college_id, name, github_url, linkedin_url, bio) VALUES 
(3, 1, 'Manvith Gowda', 'https://github.com/manvithgowda', 'https://linkedin.com/in/manvithgowda', 'Aspiring Software Engineer passionate about backend systems and distributed architecture.')
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO student_skills (student_id, skill_id, proficiency) VALUES 
(3, 1, 'ADVANCED'),
(3, 2, 'ADVANCED')
ON CONFLICT (student_id, skill_id) DO NOTHING;

-- 7. Seed Sample Hiring Challenge Event
INSERT INTO events (event_id, organization_id, created_by, title, description, event_type, event_mode, event_date, registration_deadline, location, max_participants, status, approved_by, approved_at, created_at, updated_at) VALUES 
(1, 1, 2, 'National Systems & Backend Hiring Challenge 2026', 'High-velocity 3-stage competition for top engineers. Direct hiring offers extended to top performers.', 'HIRING_CHALLENGE', 'ONLINE', NOW() + INTERVAL '14 days', NOW() + INTERVAL '10 days', 'Remote', 500, 'LIVE', 1, NOW(), NOW(), NOW())
ON CONFLICT (event_id) DO NOTHING;

-- 8. Seed Event Rounds
INSERT INTO event_rounds (round_id, event_id, round_number, name, round_type, description, start_time, end_time, duration_minutes, total_marks, passing_marks, status, created_at, updated_at) VALUES 
(1, 1, 1, 'CS Fundamentals & Aptitude', 'APTITUDE', '60 questions evaluating algorithms, operating systems, and DBMS', NOW() + INTERVAL '14 days', NOW() + INTERVAL '14 days 1 hour', 60, 100.0, 60.0, 'UPCOMING', NOW(), NOW()),
(2, 1, 2, 'Algorithmic Coding Arena', 'CODING', '3 algorithmic coding problems with hidden test case evaluation', NOW() + INTERVAL '15 days', NOW() + INTERVAL '15 days 2 hours', 120, 100.0, 50.0, 'UPCOMING', NOW(), NOW()),
(3, 1, 3, 'Technical & System Design Interview', 'INTERVIEW', '1-on-1 live technical interview with senior engineering leads', NOW() + INTERVAL '17 days', NOW() + INTERVAL '18 days', 45, 100.0, 70.0, 'UPCOMING', NOW(), NOW())
ON CONFLICT (round_id) DO NOTHING;

COMMIT;
