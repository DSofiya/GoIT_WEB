"""Знайти середній бал у групах з певного предмета."""
SELECT
  g.id,
  g.name ,
  ROUND(AVG(gr.grade), 2) AS average_grade
FROM
  grades gr
JOIN
  students s ON gr.student_id = s.id
JOIN
  groups g ON s.group_id = g.id
JOIN
  subjects sub ON gr.subject_id = sub.id
WHERE
  sub.id = 1 -- Предмет від1 до 5
GROUP by
  g.id;
