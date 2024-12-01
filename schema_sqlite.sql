-- lecturers definition

CREATE TABLE "lecturers" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nidn INTEGER NOT NULL,
	name TEXT NOT NULL,
	major TEXT NOT NULL
	faculty TEXT NOT NULL
);

CREATE UNIQUE INDEX lecturer_nidn_IDX ON "lecturers" (nidn);


-- students definition

CREATE TABLE students (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	faculty TEXT NOT NULL,
	major TEXT NOT NULL,
	generation INTEGER NOT NULL,
	gpa INTEGER NOT NULL,
	status TEXT NOT NULL,
	graduation_year INTEGER,
	graduation_semester INTEGER
);


-- lecturer_researches definition

CREATE TABLE "lecturer_researches" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nidn INTEGER NOT NULL,
	title TEXT NOT NULL,
	publication_date TEXT NOT NULL,
	publication_type TEXT NOT NULL,
	publication_detail TEXT NOT NULL,
	CONSTRAINT lecturer_research_lecturer_FK FOREIGN KEY (nidn) REFERENCES "lecturers"(id)
);

CREATE INDEX lecturer_research_nidn_IDX ON "lecturer_researches" (nidn);


-- student_activities definition

CREATE TABLE student_activities (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	student_id INTEGER NOT NULL,
	bank_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	"type" TEXT NOT NULL,
	date TEXT NOT NULL,
	CONSTRAINT student_activities_students_FK FOREIGN KEY (student_id) REFERENCES students(id)
);
