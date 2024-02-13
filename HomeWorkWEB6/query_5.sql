"""Знайти які курси читає певний викладач."""

select
  t.fullname,
  s.name 
FROM
   subjects s
JOIN
  teachers t  ON s.teacher_id = t.id
WHERE
  t.id = 1 -- Предмет від1 до 5
GROUP by
  s.name,
  t.id;