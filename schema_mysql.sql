-- lecturers definition

CREATE TABLE lecturers (
	id BIGINT NOT NULL AUTO_INCREMENT,
	nidn BIGINT NOT NULL,
	name VARCHAR(255) NOT NULL,
	major VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE UNIQUE INDEX lecturer_nidn_IDX ON lecturers (nidn);

CREATE TABLE students (
	id BIGINT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	faculty VARCHAR(255) NOT NULL,
	generation INT NOT NULL,
	gpa DECIMAL(3,2) NOT NULL,
	status VARCHAR(50) NOT NULL,
	graduation_year INT,
	graduation_semester INT,
	PRIMARY KEY (id)
) ENGINE=InnoDB;

-- lecturer_researches definition

CREATE TABLE lecturer_researches (
	id BIGINT NOT NULL AUTO_INCREMENT,
	nidn BIGINT NOT NULL,
	title TEXT NOT NULL,
	publication_date DATE NOT NULL,
	publication_type VARCHAR(100) NOT NULL,
	publication_detail TEXT NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT lecturer_research_lecturer_FK FOREIGN KEY (nidn) REFERENCES lecturers(nidn)
) ENGINE=InnoDB;

CREATE INDEX lecturer_research_nidn_IDX ON lecturer_researches (nidn);

-- student_activities definition

CREATE TABLE student_activities (
	id BIGINT NOT NULL AUTO_INCREMENT,
	student_id BIGINT NOT NULL,
	bank_id INT NOT NULL,
	name TEXT NOT NULL,
	type VARCHAR(100) NOT NULL,
	date DATE NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT student_activities_students_FK FOREIGN KEY (student_id) REFERENCES students(id)
) ENGINE=InnoDB;
