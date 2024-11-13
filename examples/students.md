age;semester;study_hours;sleep_hours;attendance;grade
{% for _ in range(500) -%}

    {# Attributes #}
    {%- set base_study_hours = gauss(5, 2) -%}
    {%- set base_sleep_hours = 7 + gauss(0, 1) - (base_study_hours - 5) * 0.3 -%}

    {%- set study_hours = max(1, round(base_study_hours, 1)) -%}
    {%- set sleep_hours = max(4, min(10, round(base_sleep_hours, 1))) -%}

    {%- set age = 18 + iuniform(0, 15) -%}
    {%- set base_semester = (age - 18) // 2 + 1 -%}
    {%- set semester_variation = itriangular(-1, 1) -%}
    {%- set semester = max(1, min(10, base_semester + semester_variation)) -%}

    {%- set attendance      = int(20 + uniform(0, 80)) -%}

    {%- set age_attendance_bonus  = (age - 24) * 0.4 -%}
    {%- set age_study_bonus       = (age - 20) * 0.3 -%}

    {%- set age_attendance_bonus = 20 / (1 + exp(-(age - 23) / 2)) - 10 -%}
    {%- set age_study_bonus      = 15 / (1 + exp(-(age - 21) / 3)) - 7.5 -%}

    {%- set base_grade      = gauss(30, 10) -%}
    {%- set study_factor    = round((study_hours ** 0.8) * 2 if study_hours > 2 else -10, 1) -%}
    {%- set sleep_factor    = 15 - (abs(sleep_hours - 7) ** 1.5) -%}
    {%- set age_factor      = (age - 21) * 2 if age > 21 else (age - 18) -%}
    {%- set semester_factor = -2.5 * (semester - 6) if semester > 6 else (6 - semester) * 2 -%}
    {%- set attendance_factor = (attendance / 100) * 25 + (attendance - 70) * 0.2 -%}

    {%- set grade = base_grade + study_factor + sleep_factor + age_factor + semester_factor + attendance_factor -%}
    {%- set grade = round(min(max(1, grade), 100), 1) -%}

    {{ age }};{{ semester }};{{ study_hours }};{{ sleep_hours }};{{ attendance }};{{ grade }}
{% endfor %}
