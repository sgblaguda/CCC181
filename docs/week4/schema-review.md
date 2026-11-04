# Schema self-review

My starting point was ClinicQ's three tables. These are the problems I found when I reviewed them for Qeazy.

## Users: who is a person?

**Works well:** `student_id` is NOT NULL and UNIQUE, so a returning student is recognized and cannot have two accounts, and `created_at` gives me a date for the 30-day deletion rule.

**Problem:** ClinicQ makes `email` NOT NULL UNIQUE and treats it as the identity. In Qeazy the email is optional (FR-13), so students without one could not join, and two students with no email would break UNIQUE.

**Change:** `student_id` is now the unique identity, and `email` is a nullable column with no UNIQUE.

## Deleting people without losing history

**Works well:** Tickets stay linked to the person only through `user_id`, so the data about waits and statuses is separate from personal details.

**Problem:** ClinicQ's rule blocks deleting a user who has tickets (RESTRICT). That conflicts with my NFR-03, which says personal records must be deleted within 30 days, and with the staff's need for old tickets in reports.

**Change:** `tickets.user_id` is nullable with ON DELETE SET NULL, so removing a person keeps the ticket for reports. The `services` foreign key stays RESTRICT, because deleting a service must not erase its tickets.

## Two kinds of delete for tickets

**Works well:** The schema already has what a soft delete needs: a `status` column that can say a ticket is finished without removing the row.

**Problem:** A ticket can disappear for two different reasons. A student who leaves the queue is real history that the staff need for reports. A test ticket or one created by mistake is not history, and keeping it would make the counts wrong.

**Change:** Leaving the queue is a soft delete: the status becomes `left` and the row stays in `tickets`. Staff can also hard delete a mistaken ticket from the dashboard, after a confirmation. Both are POST routes. The hard delete does not touch `users`, because the foreign key points from the ticket to the person and not the other way around.

## Switching a service off

**Works well:** `tickets.service_id` is RESTRICT, so a service with tickets can never be deleted by accident and old tickets always have a service to point to.

**Problem:** The same rule means staff had no way to stop offering a concern for a semester. They could not delete it, and leaving it in the list let students join a queue nobody was serving. FR-11 also asks for staff to be able to switch a concern off.

**Change:** I added `services.active`, a boolean NOT NULL DEFAULT true, in a second migration. It has a `server_default` because the table already had rows, and PostgreSQL needs a value to put in them. The join form shows only active services, and `join` rejects an inactive one the same way as one that does not exist. The dashboard and Manage services still list all services, so old tickets keep their concern name. A service with no tickets can still be deleted. One with tickets is refused with a message telling staff to switch it off instead.

## Position in line

**Works well:** There is no `position` column, the number of people ahead is computed from the tickets.

**Problem:** If I order the queue only by `created_at`, two students who join in the same instant could tie, and each would be counted ahead of the other.

**Change:** I will count people ahead by the ticket `id`, which is unique and always in join order. `created_at` stays for showing the time joined and for reports. "Call next" picks the oldest waiting ticket by `created_at`, with `id` as the tiebreaker.

## Statuses and what is left out

**Works well:** A CHECK constraint limits `status` to five known values, so a typo can never reach the table. Calling a ticket also sets `called_at`, so the time it was called is stored as a fact and not worked out later.

**Problem:** In Week 3, leaving the queue set the status to `no-show`, which mixes "left on their own" with "did not come when called", and the daily report (FR-06) needs them apart.

**Change:** I added a separate `left` status, and leaving the queue now sets it (see the soft delete above). I did not add a `role` column or a staff table; they come with login in Week 11. Until then the staff pages, including Manage services, are open to everyone, and a GitHub issue tracks that.