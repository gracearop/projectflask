
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS voice_commands;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS lecturer;

CREATE TABLE student (
  student_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_name TEXT UNIQUE NOT NULL,
  student_password TEXT NOT NULL,
  matric_number TEXT UNIQUE NOT NULL,
  student_level INTEGER NOT NULL,
  student_state TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  programme_type TEXT NOT NULL,
  department TEXT NOT NULL,
  local_government TEXT NOT NULL,
  phone_number TEXT UNIQUE NOT NULL,
  year_of_admission INTEGER NOT NULL,
  faculty TEXT NOT NULL,
  programme TEXT NOT NULL,
  profile_image BLOB -- Column to store the profile image
);

-- Create the voice_commands table to store voice commands
CREATE TABLE voice_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    voice_command TEXT NOT NULL,
    target_url TEXT NOT NULL,
    command_description TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student (student_id)

);

-- Create the results table with student_id as a foreign key
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    lecturer_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    semester TEXT NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (student_id)
    FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id)
);

-- Create the lecturers table to store lecturer information
CREATE TABLE lecturer (
    lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_number TEXT UNIQUE NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


