-- DELETE ALL
DELETE FROM sturm.polls_passwordresettoken;
DELETE FROM sturm.polls_scores;
DELETE FROM sturm.polls_questions;
DELETE FROM sturm.polls_unansweredquestions;
DELETE FROM sturm.polls_searched;
DELETE FROM sturm.polls_history;
DELETE FROM sturm.polls_student;

-- RESET INCREMENT
ALTER TABLE sturm.polls_passwordresettoken AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_scores AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_questions AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_unansweredquestions AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_searched AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_history AUTO_INCREMENT = 1;
ALTER TABLE sturm.polls_student AUTO_INCREMENT = 1;

-- ADD ADMIN
INSERT INTO sturm.polls_student (username, name, surname, email, password, status)
 VALUES ('admin1', 'Admin', 'Admin', 'kn233091m@student.etf.bg.ac.rs', 'pbkdf2_sha256$720000$qlrIdLXQhCCDTRdmvR7A72$u5XC6YLh9bFkScjweu25IdjmS9nUi81TraulQSI2250=', 'STUDENT');
