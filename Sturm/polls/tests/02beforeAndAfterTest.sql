SET SQL_SAFE_UPDATES = 0;

-- DELETE TOKEN
DELETE FROM sturm.polls_passwordresettoken WHERE user_id = (
select id
from sturm.polls_student
where email = 'kn233091m@student.etf.bg.ac.rs'
);

-- DELETE SCORE
DELETE FROM sturm.polls_scores WHERE idStudent = (
select id
from sturm.polls_student
where username = 'testReg123'
);

-- DELETE QUESTIONS
DELETE FROM sturm.polls_questions WHERE idStudent = (
select id
from sturm.polls_student
where username = 'testReg123'
);

-- DELETE UNASWERED QUESTIONS
DELETE FROM sturm.polls_unansweredquestions WHERE idStudent = (
select id
from sturm.polls_student
where username = 'testReg123'
);

-- DELETE SEARCHED
DELETE FROM sturm.polls_searched WHERE idStudent = (
select id
from sturm.polls_student
where username = 'testReg123'
);

-- DELETE HISTORY
DELETE FROM sturm.polls_history WHERE idStudent = (
select id
from sturm.polls_student
where username = 'testReg123'
);

-- DELETE STUDENT
DELETE FROM sturm.polls_student WHERE  username = 'testReg123';
