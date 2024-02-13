"""Знайти студента із найвищим середнім балом з певного предмета."""

SELECT 
    s.id, 
    s.fullname, 
    ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
where g.subject_id = 5 --Предмет від 1 до 5
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 1;