"""Список курсів, які певному студенту читає певний викладач."""
select
  s.fullname,
  t.fullname,
  sub.name
FROM
  students s
JOIN
  grades g  ON  g.student_id = s.id
JOIN
  subjects sub  ON g.subject_id = sub.id 
JOIN
  teachers t  ON sub.teacher_id = t.id
WHERE
  s.id = 13 and t.id = 1-- Студент  від 1 до 50, Вчитель від 1 до 3
GROUP by
  g.grade,
  t.fullname,
  sub.name,
  s.fullname;