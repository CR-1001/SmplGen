INSERT INTO employee (employee_id, first_name, last_name, email, hire_date, job_title) VALUES
{%- for i in range(10) %}
    ({{count()}}, '{{first_name()}}', '{{last_name()}}', '{{email()}}', '{{day()}}", '{{choice(['Admin', 'Developer', 'Tester'])}}'),
{%- endfor %}
;
