from sqlalchemy import func, desc, select, and_

from confa.models import Grade, Teacher, Student, Group, Subject
from confa.db import session


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .filter(Grade.subjects_id == 1)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
        .all()
    )
    return result


def select_03():
    """
    SELECT
    g.id,
    g.name ,
    ROUND(AVG(gr.grade), 2) AS average_grade
    FROM
    grades gr
    JOIN students s ON gr.student_id = s.id
    JOIN groups g ON s.group_id = g.id
    JOIN subjects sub ON gr.subject_id = sub.id
    WHERE sub.id = 1 -- Предмет від1 до 5
    GROUP by g.id;
    """
    result = (
        session.query(
            Group.id,
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .filter(Subject.id == 1)
        .group_by(Group.id)
        .all()
    )
    return result


def select_04():
    """select
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
    """
    result = (
        session.query(Teacher.fullname, Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == 1)
        .group_by(Subject.name, Teacher.id)
    )

    return result


def select_05():
    """
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
    """
    result = (
        session.query(Teacher.fullname, Subject.name)
        .join(Subject, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == 1)
        .group_by(Teacher.fullname, Subject.name)
        .all()
    )

    return result


def select_06():
    """
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
    """
    result = (
        session.query(Group.id, Student.fullname)
        .join(Student, Student.group_id == Group.id)
        .filter(Group.id == 1)
        .group_by(Student.fullname, Group.id)
        .all()
    )

    return result


def select_07():
    """
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

    """
    result = (
        session.query(Group.name, Subject.name, Student.fullname, Grade.grade)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .filter(Group.id == 1, Subject.id == 1)
        .group_by(Group.name, Grade.grade, Subject.name, Student.fullname, Group.id)
        .all()
    )
    return result


def select_08():
    """
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
    t.id = 1
    GROUP by
    s.name,
    t.id;
    """
    result = (
        session.query(
            Teacher.fullname,
            Subject.name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .join(Subject, Subject.id == Grade.subjects_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.id == 1)
        .group_by(Subject.name, Teacher.id)
        .all()
    )
    return result


def select_09():
    """
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
    s.id = 13
    GROUP by
    g.grade,
    sub.name,
    s.fullname;
    """
    result = (
        session.query(Student.fullname, Subject.name)
        .join(Grade, Grade.subjects_id == Student.id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .filter(Student.id == 13)
        .group_by(Grade.grade, Subject.name, Student.fullname)
        .all()
    )
    return result


def select_10():
    """
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
    s.id = 13 and t.id = 1
    GROUP by
    g.grade,
    t.fullname,
    sub.name,
    s.fullname;
    """
    result = (
        session.query(Student.fullname, Teacher.fullname, Subject.name)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subjects_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.id == 13, Teacher.id == 1)
        .group_by(Grade.grade, Teacher.fullname, Subject.name, Student.fullname)
        .all()
    )
    return result


def select_11():
    """
    select
    st.fullname,
    s.teacher_id,
    ROUND(AVG(gr.grade), 2) AS average_grade
    FROM
    grades gr
    JOIN
    subjects s  ON gr.subject_id = s.id
    JOIN
    students st  ON gr.student_id = st.id
    WHERE
    s.teacher_id = 1 and st.id = 13
    GROUP by
    st.fullname,
    s.teacher_id;
    """
    result = (
        session.query(
            Student.fullname,
            Subject.teacher_id,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .join(Subject, Subject.id == Grade.subjects_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Subject.teacher_id == 1, Student.id == 13)
        .group_by(Student.fullname, Subject.teacher_id)
        .all()
    )
    return result


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student)
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3))
    ).scalar_subquery()

    result = (
        session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date)
        .select_from(Grade)
        .join(Student)
        .filter(
            and_(
                Grade.subjects_id == 2,
                Student.group_id == 3,
                Grade.grade_date == subquery,
            )
        )
        .all()
    )

    return result


if __name__ == "__main__":
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_11())
    print(select_12())
