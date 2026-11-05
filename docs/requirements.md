# Qeazy requirements

**Setting:** School registrar office. Enrollment and form requests are online, but forms are submitted in person and some enrollment concerns (late enrollment, change of subjects, crediting, record correction) can only be settled at the counter.
**People who wait:** Students with an in-person enrollment concern. Persona: Loi, in [docs/week3/personas.md](week3/personas.md).
**People who serve:** Registrar staff. Persona: Rina, in [docs/week3/personas.md](week3/personas.md).

**Problem statement:** A student with an enrollment concern that must be settled in person needs a way to know when they will be served and to arrive with complete requirements, because the uncertainty of not knowing the wait makes them stay in line for hours and risk being sent back at the end.

## Functional requirements

IDs FR-01 to FR-07 are from my Week 1 proposal and keep their meaning. FR-08 onward are new.

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue for a type of concern from their phone. | Must | **Yes** | Built (Week 3) |
| FR-02 | A student can see their ticket number, status, how many people are ahead of them and the estimated wait. | Must | **Yes** | Built (Week 3) |
| FR-03 | Registrar staff can call the next waiting student, see their concern, and mark them as served or no-show. | Must | **Yes** | Built (Week 3) |
| FR-04 | A student is notified when their turn is near. | Should | No (uses stored email, see FR-13) | Later |
| FR-05 ★ | A student can see the forms needed for their type of concern before joining. | Should | No (fixed list in the page for now) | Later |
| FR-06 | The registrar head can see daily counts of students served and average waiting time. | Could | No (computed from tickets) | Later |
| FR-07 | A student can submit forms or documents inside the app. | Won't (this semester) | Yes | Dropped for this semester |
| FR-08 | A student can leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| FR-09 | Staff can filter the queue by type of concern. | Should | No (reads tickets) | Built (Week 3) |
| FR-10 ★ | Staff can see how many students are waiting for each type of concern. | Should | No (computed from tickets) | Built (Week 3) |
| FR-11 | Staff can add, rename and switch off a type of concern. | Must | **Yes** | This week |
| FR-12 | A student can find their ticket again with their ticket number and student ID. | Should | **Yes** | Built (Week 3) |
| FR-13 ★ | A student can optionally give an email address for updates about their ticket. | Could | **Yes** | Built (Week 3, stored only) |
| FR-14 | Staff can delete a ticket that was created by mistake. | Should | **Yes** | This week |
| FR-15 ★ | A student is warned when they are unlikely to be served before the registrar closes. | Should | No (computed from the queue and average minutes) | Later |
| FR-16 | A student's ticket and personal details are removed 30 days after they join, while the counts for reports are kept. | Should | **Yes** | This week (schema), Later (the cleanup job) |

★ = specific to the registrar setting.

## Non-functional requirements

NFR-01 to NFR-04 are from my Week 1 proposal. NFR-05 onward are new.

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | A student's position and estimate update within 5 seconds of staff calling the next student. (Week 3 refreshes every 10 seconds, so this is not met yet.) | Performance | Should |
| NFR-02 | A first-time student can join the queue in 3 taps or fewer after opening the page, with no account. | Usability | Must |
| NFR-03 | The app collects only name, student ID, type of concern and an optional email; staff pages require login (Week 11); personal records are deleted within 30 days, in line with RA 10173. | Security / privacy | Must |
| NFR-04 | The app works in the latest two versions of Chrome and Safari on Android and iOS, and on screens as small as 360 px wide. | Compatibility | Must |
| NFR-05 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-06 | Two students can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-07 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-08 | No password or secret key is stored in the repository. | Security | Must |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-08 and FR-11, with NFR-02, NFR-05 and NFR-06. A student can join, see their place and leave, staff can call and serve students and manage the list of concerns, and no ticket is lost. This is the smallest version that solves the problem, because it removes the not-knowing and keeps the queue fair.

**Out of scope this semester:**
- Online form or document submission (FR-07), because it is a separate problem that would change the registrar's existing process.
- Staff login and roles, because they come in Week 11; the staff pages are open until then.
- Notifications by email or SMS (FR-04), because they need a mail service and extra cost; this week the email is only stored.

## Checked with a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Loi| There was no visible way to check their place from the main page.| Added a button to allow users to go back to the myplace page. (FR-12) |