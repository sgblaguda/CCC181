## Loi, the person waiting

> "Kapoy maglinya unya dili ra diay ka i-serve in the end kay sarado na diay" *"It's tiring to wait in line then in the end you won't get served because they're already closing."*

| | |
| --- | --- |
| **Photo or sketch** | ![Person waiting in line, frustrated](images/womanwaiting.png) |
| **Age, role and background** | 20, 2nd-year college student. Enrolled through the online portal like everyone else, but has a problem that cannot be settled online, such as a late enrollment, a change of subjects, a record to be corrected, or an unsettled liability. |
| **Goals** | 1. Get their enrollment problem resolved at the registrar in one visit.<br>2. Know when they will be served so they can attend their classes and do other enrollment tasks in the meantime.<br>3. Be sure that they have the reight forms and signatures before they line up. |
| **Frustrations** | 1. Their problem is time-sensitive, but they cannot tell how long the line will take or whether they will be served before the office closes.<br>2. Because most students enroll online, they are not sure when the office is busy so they often arrive to a long line.<br>3. One missing form or signature sends them back to the end of the line. |
| **Devices and context** | Smartphone, on mobile data or weak campus Wi-Fi. They are standing in or near the registrar between classes, often holding forms in one hand. |
| **Tech comfort** | Medium. They use the school portal and online forms comfortably, but will not install or sign up for a new app just to wait in line. |
| **Accessibility needs** | One hand is busy holding the forms, bright outdoor light and crowded lines, noisy hallways, slow and/or unstable connection, low-end phone. Needs easy one-handed and high contrast interface, concise language, and no account creation. |

### Scenario

Loi enrolled online and has already printed their COR, which means they're officially enrolled. However, they realized that they carry units below the required load, which means Loi has to add a subject so they can meet the required units. Their next class starts in two hours. Loi arrives at the registrar and scans the QR code posted at the entrance, and Qeazy opens in their browser without any installation. They pick `"Enrollment concern"`, sees the list of forms they need, and notices they are missing a signature, so they get it first. Back in the app, they join the queue and sees `"You are number 12, about 35 minutes until you are catered with."` on one screen. Loi goes to eat and returns to their class on time, glancing at the page to see their position drop. When it shows their turn is near, they walk back, hands in the complete forms, and is served in one visit.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Check the forms needed for my enrollment concern | Requirements checklist | FR-05 |
| Join the registrar queue from my phone | Join | FR-02 |
| See my queue number, position, and estimated wait time | My place | FR-02 |
| Get notified when my turn is near | My place (alert) | FR-04

### What this means for my interface

1. Because Loi's concern is time-sensitive and they have a class soon, my interface must show their queue number, position, and estimated wait in large text on a single screen, updating within 5 seconds, and warn them if they are unlikely to be served before the registrar closes.
2. Because they are holding forms and standing in a crowded hallway, my interface must use large tap targets and let Loi join the queue in 3 taps or fewer, without the need of creating an account.
3. Because a missing form sends them to the back of the line and their connection is unreliable, my interface must show the checklist for their type of concern before they join, work in a phone browser on weak data, and keep their place if the page reloads.


## Rina, the staff member

> (Not from an interview), during the enrollment season I've observed that staff usually need to cater to students who aren't lined up in an orderly manner which makes their job hectic.

| | |
| --- | --- |
| **Photo or sketch** | ![Illustration of what it looks like, but much more hectic](images/staff.png).  |
| **Age, role and background** | 35, registrar staff member. Handles the concerns that the online portal and online forms cannot settle, such as late enrollment, change of subjects, crediting of subjects, and record correction. Checks forms and signatures at the counter and serves students one at a time. |
| **Goals** | 1. Serve students in a fair, orderly sequence without anyone cutting the line.<br>2. Process each student without constant interruptions from people asking how long the wait is.<br>3. Know how many students are waiting and what they need, so they can plan the day. |
| **Frustrations** | 1. Enrollment concerns are urgent for students, so they crowd the counter and keep asking when their turn is.<br>2. Keeping track of who is next on paper or from memory leads to disputes about skipping or cutting the line.<br>3. Students arrive with incomplete forms or signatures, or leave and do not come back when called, which wastes time at the counter. |
| **Devices and context** | Desktop or laptop at the counter on office Wi-Fi, and sometimes a phone while away from the counter. They switch between serving a student and looking at the screen, with only a few seconds between students. |
| **Tech comfort** | Medium. They are comfortable with the school's portal and online forms, but have little time or patience to learn a new tool during enrollment season. |
| **Accessibility needs** | Reads from a screen all day, so needs large and clear text. Hands are often busy with paperwork, so each action should take one click or tap. Works in a noisy, busy office and may be interrupted at any time. |

### Scenario

Rina opens the Qeazy dashboard at the start of the day, and the list of students who joined the queue is already there, each with the type of concern they chose. The counts at the top show that three students are waiting for a change of subjects and two for late enrollment. After finishing with a student, Rina clicks **Call Next**, and ticket #12, Loi, with an add-subject concern, appears at the top of the list. Loi walks to the counter with the complete forms, and Rina checks them and clicks **Serve**. Later, ticket #13 does not show up when called, so Rina taps **No-show** and moves on to the next student. Fewer students crowd the counter asking about their turn, because they can see their own place and estimated wait on their phones. At the end of the day, Rina can see how many students were served.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Call the next student in line | Staff dashboard | FR-03 |
| Mark a student as served or no-show | Staff dashboard | FR-03 |
| See how many students are waiting and what they need | Staff dashboard | FR-03 |
| Filter the queue by type of concern | Staff dashboard | FR-03 |
| View daily served counts and average waiting time | Reports (This is not in MVP) | FR-06 |

### What this means for my interface

1. Because Rina has only a few seconds between students and their hands are busy with paperwork, my interface must make **Call Next** the largest, easiest-to-reach button and let them serve or skip a student with one click or tap.
2. Because they work on a busy counter and get interrupted often, my interface must show the current queue, each student's type of concern, and the waiting count per concern in large, clear text on one screen without extra navigation.
3. Because students may leave and not come back when called, my interface must make **No-show** quick to use and keep the queue order fair and visible, so disputes about who is next are rare.