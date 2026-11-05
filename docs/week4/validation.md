# Validation

**Setup:** Qeazy running with `flask --app app run --debug` on port 5000, PostgreSQL 17 in Docker, tested on a Mac. Date tested: 11/05/2026

## 1\. Browser layer

The form attributes match the column sizes and NOT NULL rules.

| Field | Column | Attributes in the form |
| :---- | :---- | :---- |
| Your name | `users.name` varchar(80) NOT NULL | `required`, `maxlength="80"` |
| Student ID | `users.student_id` varchar(20) NOT NULL UNIQUE | `required`, `maxlength="20"` |
| Email | `users.email` varchar(120), optional | `type="email"`, `maxlength="120"`, not required |
| Type of concern | `tickets.service_id` NOT NULL | `required` on the select |
| Concern name (Manage concerns) | `services.name` varchar(60) NOT NULL UNIQUE | `required`, `maxlength="60"` |

## 2\. Flask layer (skipping the form with curl)

| Rule | Layer | How I tested it | What happened |
| :---- | :---- | :---- | :---- |
| Name, email and concern must be valid | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=" -d "email=not-an-email" -d "service_id=999"` | `HTTP/1.1 400 BAD REQUEST` |
| Student ID must be letters, numbers and dashes | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d 'name=Mika' -d 'student_id=bad id!!' -d 'service_id=1'` | `HTTP/1.1 400 BAD REQUEST` |
| Name must be 80 characters or fewer | Flask | `curl` with a 200-character name | `HTTP/1.1 400 BAD REQUEST` |
| All fields are required | Flask | `curl -i -X POST http://127.0.0.1:5000/join` with no data | `HTTP/1.1 400 BAD REQUEST` |
| A switched-off concern cannot be joined | Flask | `curl` with the `service_id` of a concern that is switched off | `HTTP/1.1 400 BAD REQUEST` |
| Data only changes with POST | Flask | `curl -i http://127.0.0.1:5000/staff/call-next` | `HTTP/1.1 405 METHOD NOT ALLOWED` |
| Only known staff actions are accepted | Flask | `curl -i -X POST http://127.0.0.1:5000/staff/tickets/1/bogus` | `HTTP/1.1 400 BAD REQUEST` |
| A missing ticket is a 404, not a crash | Flask | `curl -i http://127.0.0.1:5000/queue/99999` | `HTTP/1.1 400 BAD REQUEST` |

## 3\. Database layer (skipping Flask with psql)

Run with `docker compose exec db psql -U qeazy`. Each of these must fail with an `ERROR`.

| Rule | Layer | How I tested it | What happened |
| :---- | :---- | :---- | :---- |
| A ticket needs a real concern | FOREIGN KEY | `INSERT INTO tickets (user_id, service_id) VALUES (1, 999);` | `ERROR:  insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` and `DETAIL:  Key (service_id)=(999) is not present in table "services".`  |
| Status must be one of five values | CHECK | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Average minutes must be above 0 | CHECK | `INSERT INTO services (name, avg_minutes) VALUES ('Test', 0);` | `ERROR:  new row for relation "services" violates check constraint "ck_services_avg_minutes"` |
| One user per student ID | UNIQUE | `INSERT INTO users (name, student_id) VALUES ('Copy', '<an existing student id>');` | `ERROR:  duplicate key value violates unique constraint "users_student_id_key"` |
| One concern per name | UNIQUE | `INSERT INTO services (name) VALUES ('Late enrollment');` | `ERROR:  duplicate key value violates unique constraint "services_name_key"` |
| A user needs a name | NOT NULL | `INSERT INTO users (name, student_id) VALUES (NULL, '2023-0002');` | `ERROR:  null value in column "name" of relation "users" violates not-null constraint` |
| A concern with tickets cannot be deleted | ON DELETE RESTRICT | `DELETE FROM services WHERE id = 1;`  | `ERROR:  update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
| Removing a person keeps their tickets | ON DELETE SET NULL | delete a test user who has a ticket, then `SELECT id, user_id, status FROM tickets;` | Users are deleted but `id`, `user_id`, and `status` are kept |

A good insert fills in the defaults:

```sql
INSERT INTO tickets (user_id, service_id) VALUES (1, 1) RETURNING id, status, created_at;
```

Result:

 `id | status  |          created_at`             
`----+---------+-------------------------------`  
  `9 | waiting | 2026-11-05 10:48:00.889202+00`

## 4\. No SQL in f-strings

Gluing user input into a SQL string lets the input become code (SQL injection). SQLAlchemy sends values separately from the SQL, so this does not happen. I checked that my code never builds SQL by hand using the command:

```
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

It printed nothing, which is the expected outcome.

## Which error was most useful

I find the error below to be most useful since it makes sure that no duplicates are made when data is input using PSQL.

```
ERROR:  duplicate key value violates unique constraint "<variable>"
```

