"""Знайти оцінки студентів у окремій групі з певного предмета."""
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
  gr.id = 1 and sub.id = 1 -- sub -Предмет від 1 до 5\ gr-Група від1 до 3
GROUP by
  gr.name,
  g.grade,
  sub.name,
  s.fullname,
  gr.id;
