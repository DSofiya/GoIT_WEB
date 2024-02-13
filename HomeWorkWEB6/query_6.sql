"""Знайти список студентів у певній групі."""
select
  gr.id,
  s.fullname
FROM
   groups gr
JOIN
  students s  ON s.group_id = gr.id
WHERE
  gr.id = 1 -- Предмет від1 до 5
GROUP by
  s.fullname,
  gr.id;
