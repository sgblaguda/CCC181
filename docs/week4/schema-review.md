# Schema self-review (DRAFT: put the ERD away for an hour, then reread this and change it to match what you really think)

My starting point was ClinicQ's three tables. These are the problems I found when I reviewed them for Qeazy.

## Users: who is a person?

**Works well:** `student_id` is NOT NULL and UNIQUE, so a returning student is recognized and cannot have two accounts, and `created_at` gives me a date for the 30-day deletion rule.


**Problem:** ClinicQ makes `email` NOT NULL UNIQUE and treats it as the identity. In Qeazy the email is optional (FR-13), so students without one could not join, and two students with no email would break UNIQUE.


**Change:** `student_id` is now the unique identity, and `email` is a nullable column with no UNIQUE.

## Deleting people without losing history

**Works well:** Tickets stay linked to the person only through `user_id`, so the data about waits and statuses is separate from personal details.\
**Problem:** ClinicQ's rule blocks deleting a user who has tickets (RESTRICT). That conflicts with my NFR-03, which says personal records must be deleted within 30 days, and with the staff's need for old tickets in reports.


**Change:** `tickets.user_id` is nullable with ON DELETE SET NULL, so removing a person keeps the ticket for reports. The `services` foreign key stays RESTRICT, because deleting a service must not erase its tickets.

## Position in line

**Works well:** There is no `position` column, the number of people ahead is computed from the tickets.


**Problem:** If I order the queue only by `created_at`, two students who join in the same instant could tie, and each would be counted ahead of the other.


**Change:** I will count people ahead by the ticket `id`, which is unique and always in join order. `created_at` stays for showing the time joined and for reports.

## Statuses and what is left out

**Works well:** A CHECK constraint limits `status` to five known values, so a typo can never reach the table.


**Problem:** In Week 3, leaving the queue set the status to `no-show`, which mixes "left on their own" with "did not come when called", and the daily report (FR-06) needs them apart.

**Change:** I added a separate `left` status. I did not add a `role` column or a staff table; they come with login in Week 11.