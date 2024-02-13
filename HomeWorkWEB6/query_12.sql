"""Оцінки студентів у певній групі з певного предмета на останньому занятті."""

select
  gr.name,
  sub.name,
  s.fullname,
  g.grade 
FROM
   grades g
JOIN
  students s  ON  g.student_id = s.id
JOIN
  groups gr  ON s.group_id = gr.id
JOIN
  subjects sub  ON g.subject_id = sub.id 
where
  gr.id = 1  AND g.grade_date = (SELECT MAX(grade_date) FROM grades g WHERE subject_id = 1)
GROUP by
  gr.name,
  g.grade,
  sub.name,
  s.fullname,
  gr.id;