"""Знайти середній бал на потоці (по всій таблиці оцінок)."""

select
  ROUND(AVG(gr.grade), 2) AS average_grade
FROM
  grades gr;