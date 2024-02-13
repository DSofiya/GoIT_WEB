"""Знайти список курсів, які відвідує студент."""
select
  s.fullname,
  sub.name
FROM
  students s
JOIN
  grades g  ON  g.student_id = s.id
JOIN
  subjects sub  ON g.subject_id = sub.id 
WHERE
  s.id = 13 -- Студент  від 1 до 50
GROUP by
  g.grade,
  sub.name,
  s.fullname;