# Accessibility check (Part 9)

Screens checked: Join (`/join`), My place (`/queue/<n>`), Staff dashboard (`/staff`).

## 9a. Lighthouse (Chrome DevTools, Accessibility + Mobile)

| Screen | First score | Final score | Screenshot |
|---|---|---|---|
| Join (`/join`) | 94 | 94 | screenshots/lighthouse-join.png |
| My place (`/queue/4`) | 92 | 92 | screenshots/lighthouse-myplace.png |
| Staff (`/staff`) | 97 | 97 | screenshots/lighthouse-staff.png |

I also ran Lighthouse on the home page (`/`), which scored at a range of 92 to 97. All runs used the Mobile setting on `http://127.0.0.1:5001`.

**Issues Lighthouse listed and how I fixed them:** Lighthouse listed no accessibility issues on any screen, so I ran it once per screen and did not need to fix anything or run it again.

**Anything still below 90 and why:** None. All three screens scored above 90.

## 9b. Keyboard only

(Tested with Tab, Shift+Tab, Enter, Space and arrow keys, no mouse.)

| Step | Worked? | Notes |
|---|---|---|
| First Tab shows the "Skip to main content" link | Yes | |
| Open the menu button with Enter and reach the links | Yes | |
| Home page: reach and press "Join the queue" | Yes | |
| Join form: fill name, ID, pick a concern with arrow keys, submit with Enter | Yes | |
| Focus is clearly visible at every step | Yes | |
| Staff: use the filter select and Filter button | Yes | |
| Staff: Call Next, then Serve on the called ticket | Yes | |
| My place: reach Leave the queue | Yes | |

**What failed and how I fixed it:** Nothing failed when I tested the interface.

## 9c. Manual checklist

| Check | Join | My place | Staff |
|---|---|---|---|
| Every input has a visible label | ✅ name, student ID and concern all have `<label for>` | n/a (no inputs) | ✅ the filter has a "Filter concern" label |
| Error messages say what to do, in text | ✅ e.g. "Enter your name." under each wrong field, plus a red alert | n/a | ✅ warning alerts in words (e.g. "No one is waiting.") |
| Status is shown in words, not only color | n/a | ✅ badge text says Waiting / Called / Served / No-show | ✅ badge text says Waiting / Called |
| Readable at 375 px with no sideways page scroll |  ✅ disabled through a css tag| ✅ disabled through a css tag| ✅ disabled through a css tag |
| Buttons at least about 44 × 44 px on a phone | ✅| ✅| ✅ |
| One `<h1>` and headings in order | ✅ | ✅ | ✅ |
| `<html lang="en">` is set | ✅ in `base.html` | ✅ | ✅ |