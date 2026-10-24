## Loi, the person waiting

> "Kapoy maglinya unya dili ra diay ka i-serve in the end kay sarado na diay" *"It's tiring to wait in line then in the end you won't get served because they're already closing."*

| | |
| --- | --- |
| **Photo or sketch** | ![Person waiting in line, frustrated](week3/images/womanwaiting.png) |
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