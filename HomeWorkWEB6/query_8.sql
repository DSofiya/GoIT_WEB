"""Знайти середній бал, який ставить певний викладач зі своїх предметів."""
select
  t.fullname,
  s.name, 
  ROUND(AVG(gr.grade), 2) AS average_grade
FROM
  grades gr
JOIN
  subjects s  ON gr.subject_id = s.id
JOIN
  teachers t  ON s.teacher_id = t.id
WHERE
  t.id = 1 -- Викладач від 1 до 3
GROUP by
  s.name,
  t.id;