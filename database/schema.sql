-- Proup Platform PostgreSQL Schema
-- 22 Relational Tables

BEGIN;

CREATE TABLE achievements (
	achievement_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (achievement_id)
);

CREATE TABLE colleges (
	college_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	location VARCHAR(255), 
	PRIMARY KEY (college_id)
);

CREATE TABLE organizations (
	organization_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	cin VARCHAR(64) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	website VARCHAR(255), 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (organization_id)
);

CREATE TABLE skills (
	skill_id SERIAL NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (skill_id)
);

CREATE TABLE users (
	user_id SERIAL NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(32) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (user_id)
);

CREATE TABLE blogs (
	blog_id SERIAL NOT NULL, 
	author_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	content TEXT NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (blog_id), 
	FOREIGN KEY(author_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE events (
	event_id SERIAL NOT NULL, 
	organization_id INTEGER NOT NULL, 
	created_by INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT NOT NULL, 
	event_type VARCHAR(50) NOT NULL, 
	event_mode VARCHAR(50) NOT NULL, 
	event_date TIMESTAMP WITH TIME ZONE NOT NULL, 
	registration_deadline TIMESTAMP WITH TIME ZONE NOT NULL, 
	location VARCHAR(255), 
	max_participants INTEGER, 
	status VARCHAR(50) NOT NULL, 
	approved_by INTEGER, 
	approved_at TIMESTAMP WITH TIME ZONE, 
	rejection_reason VARCHAR(500), 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (event_id), 
	FOREIGN KEY(organization_id) REFERENCES organizations (organization_id) ON DELETE CASCADE, 
	FOREIGN KEY(created_by) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(approved_by) REFERENCES users (user_id)
);

CREATE TABLE notifications (
	notification_id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	message TEXT NOT NULL, 
	type VARCHAR(50) NOT NULL, 
	is_read BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (notification_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE organizer_profiles (
	user_id INTEGER NOT NULL, 
	organization_id INTEGER NOT NULL, 
	verification_status VARCHAR(32) NOT NULL, 
	verified_by INTEGER, 
	verified_at TIMESTAMP WITH TIME ZONE, 
	rejection_reason VARCHAR(500), 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(organization_id) REFERENCES organizations (organization_id) ON DELETE RESTRICT, 
	FOREIGN KEY(verified_by) REFERENCES users (user_id)
);

CREATE TABLE student_profiles (
	user_id INTEGER NOT NULL, 
	college_id INTEGER, 
	name VARCHAR(255) NOT NULL, 
	github_url VARCHAR(255), 
	linkedin_url VARCHAR(255), 
	resume_url VARCHAR(255), 
	bio TEXT, 
	PRIMARY KEY (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(college_id) REFERENCES colleges (college_id) ON DELETE SET NULL
);

CREATE TABLE event_registrations (
	registration_id SERIAL NOT NULL, 
	event_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	attendance_status VARCHAR(32) NOT NULL, 
	registered_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (registration_id), 
	CONSTRAINT uq_event_student_registration UNIQUE (event_id, student_id), 
	FOREIGN KEY(event_id) REFERENCES events (event_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE event_results (
	result_id SERIAL NOT NULL, 
	event_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	overall_score FLOAT NOT NULL, 
	rank INTEGER, 
	feedback TEXT, 
	evaluated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (result_id), 
	FOREIGN KEY(event_id) REFERENCES events (event_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE event_rounds (
	round_id SERIAL NOT NULL, 
	event_id INTEGER NOT NULL, 
	round_number INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	round_type VARCHAR(50) NOT NULL, 
	description TEXT, 
	start_time TIMESTAMP WITH TIME ZONE NOT NULL, 
	end_time TIMESTAMP WITH TIME ZONE NOT NULL, 
	duration_minutes INTEGER NOT NULL, 
	total_marks FLOAT NOT NULL, 
	passing_marks FLOAT NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (round_id), 
	FOREIGN KEY(event_id) REFERENCES events (event_id) ON DELETE CASCADE
);

CREATE TABLE hiring (
	hiring_id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	organization_id INTEGER NOT NULL, 
	event_id INTEGER, 
	status VARCHAR(50) NOT NULL, 
	job_title VARCHAR(255) NOT NULL, 
	job_type VARCHAR(50) NOT NULL, 
	offered_at TIMESTAMP WITH TIME ZONE, 
	accepted_at TIMESTAMP WITH TIME ZONE, 
	rejected_at TIMESTAMP WITH TIME ZONE, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (hiring_id), 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(organization_id) REFERENCES organizations (organization_id) ON DELETE CASCADE, 
	FOREIGN KEY(event_id) REFERENCES events (event_id) ON DELETE SET NULL
);

CREATE TABLE student_achievements (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	achievement_id INTEGER NOT NULL, 
	event_id INTEGER, 
	certificate_url VARCHAR(500), 
	awarded_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(achievement_id) REFERENCES achievements (achievement_id) ON DELETE CASCADE, 
	FOREIGN KEY(event_id) REFERENCES events (event_id) ON DELETE SET NULL
);

CREATE TABLE student_skills (
	student_id INTEGER NOT NULL, 
	skill_id INTEGER NOT NULL, 
	proficiency VARCHAR(32) NOT NULL, 
	PRIMARY KEY (student_id, skill_id), 
	FOREIGN KEY(student_id) REFERENCES student_profiles (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE
);

CREATE TABLE assessments (
	assessment_id SERIAL NOT NULL, 
	round_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT, 
	duration_minutes INTEGER NOT NULL, 
	total_marks FLOAT NOT NULL, 
	passing_marks FLOAT NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (assessment_id), 
	FOREIGN KEY(round_id) REFERENCES event_rounds (round_id) ON DELETE CASCADE
);

CREATE TABLE interviews (
	interview_id SERIAL NOT NULL, 
	round_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	interviewer_id INTEGER NOT NULL, 
	scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	duration_minutes INTEGER NOT NULL, 
	meeting_url VARCHAR(500), 
	status VARCHAR(50) NOT NULL, 
	score FLOAT, 
	feedback TEXT, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (interview_id), 
	FOREIGN KEY(round_id) REFERENCES event_rounds (round_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(interviewer_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE round_shortlists (
	shortlist_id SERIAL NOT NULL, 
	round_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	selected_by INTEGER, 
	selected_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	remarks VARCHAR(500), 
	PRIMARY KEY (shortlist_id), 
	FOREIGN KEY(round_id) REFERENCES event_rounds (round_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(selected_by) REFERENCES users (user_id)
);

CREATE TABLE assessment_results (
	result_id SERIAL NOT NULL, 
	assessment_id INTEGER NOT NULL, 
	round_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	score FLOAT NOT NULL, 
	percentage FLOAT NOT NULL, 
	passed BOOLEAN NOT NULL, 
	rank INTEGER, 
	feedback TEXT, 
	evaluated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (result_id), 
	FOREIGN KEY(assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE, 
	FOREIGN KEY(round_id) REFERENCES event_rounds (round_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE coding_problems (
	problem_id SERIAL NOT NULL, 
	assessment_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT NOT NULL, 
	input_format TEXT, 
	output_format TEXT, 
	constraints TEXT, 
	difficulty VARCHAR(32) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (problem_id), 
	FOREIGN KEY(assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
);

CREATE TABLE questions (
	question_id SERIAL NOT NULL, 
	assessment_id INTEGER NOT NULL, 
	question_text TEXT NOT NULL, 
	question_type VARCHAR(50) NOT NULL, 
	marks FLOAT NOT NULL, 
	negative_marks FLOAT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (question_id), 
	FOREIGN KEY(assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
);

CREATE TABLE coding_submissions (
	submission_id SERIAL NOT NULL, 
	problem_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	language VARCHAR(32) NOT NULL, 
	source_code TEXT NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	test_cases_passed INTEGER NOT NULL, 
	total_test_cases INTEGER NOT NULL, 
	score FLOAT NOT NULL, 
	submitted_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (submission_id), 
	FOREIGN KEY(problem_id) REFERENCES coding_problems (problem_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE coding_test_cases (
	test_case_id SERIAL NOT NULL, 
	problem_id INTEGER NOT NULL, 
	input_data TEXT NOT NULL, 
	expected_output TEXT NOT NULL, 
	marks FLOAT NOT NULL, 
	is_hidden BOOLEAN NOT NULL, 
	PRIMARY KEY (test_case_id), 
	FOREIGN KEY(problem_id) REFERENCES coding_problems (problem_id) ON DELETE CASCADE
);

CREATE TABLE question_options (
	option_id SERIAL NOT NULL, 
	question_id INTEGER NOT NULL, 
	option_text TEXT NOT NULL, 
	is_correct BOOLEAN NOT NULL, 
	PRIMARY KEY (option_id), 
	FOREIGN KEY(question_id) REFERENCES questions (question_id) ON DELETE CASCADE
);

CREATE TABLE answers (
	answer_id SERIAL NOT NULL, 
	question_id INTEGER NOT NULL, 
	assessment_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	selected_option_id INTEGER, 
	is_correct BOOLEAN NOT NULL, 
	marks_obtained FLOAT NOT NULL, 
	submitted_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (answer_id), 
	CONSTRAINT uq_question_student_answer UNIQUE (question_id, student_id), 
	FOREIGN KEY(question_id) REFERENCES questions (question_id) ON DELETE CASCADE, 
	FOREIGN KEY(assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE, 
	FOREIGN KEY(student_id) REFERENCES users (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(selected_option_id) REFERENCES question_options (option_id) ON DELETE SET NULL
);

COMMIT;
