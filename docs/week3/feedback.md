# Part 3: Self-review of my personas and wireframes

I reviewed each screen at phone and laptop width against Loi (the student waiting) and Rina (the registrar staff member), using their "Because …, my interface must …" rules.

## Join (phone and laptop)

**Works well:** The form has only three inputs and one big **Get a Ticket** button at the bottom, within thumb reach on the phone. This follows Loi's rule that they must be able to join in 3 taps or fewer, one-handed, with no account. The checklist appears right under the concern selector, so Loi can see the missing form or signature *before* joining, which follows the rule about not being sent back to the end of the line.

**Problem:** The inputs only show their names as placeholder text inside the boxes (`[input] Your name`, `[input] Student ID`), with no visible label, so the label disappears once Loi starts typing (recognition rather than recall). Also, the checklist has tick boxes but the wireframe doesn't say what happens if Loi leaves them unticked. It's unclear whether they block **Get a Ticket**, which is an error-prevention issue. A smaller one: the checklist item "Add/Drop form" doesn't match the concern names in the wireframes ("Change of subjects"), which hurts match with the real world.

**Change:** I will add visible labels above each input and mark them in the wireframe. Add a short line under the checklist ("Check these before you go to the counter") so it's clear. I will also use the same wording for the concern and its checklist. I'm keeping the button at the bottom, since it suits one-handed use. I will also fix the requirement IDs on both Join frames from FR-02 to FR-01 (join) and FR-05 (checklist).


## My place (phone and laptop)

**Works well:** The ticket number **#12** is by far the biggest element, and the status, wait time and "11 people are ahead of you" are right below it, so Loi can understand their place in a quick glance between classes. This follows the rule that the queue number, position and wait must be large and on a single screen. Status is written in words ("Waiting"), not only color.

**Problem:** (1) The big number is labeled `[position]`, but #12 is the ticket number. The real position is "11 people are ahead of you", so the labels confuse the two (match with the real world, consistency). (2) "Your turn is near!" is always drawn on the screen, even though Loi still has 11 people ahead, which contradicts the status above it (visibility of system status). (3) Loi's first rule says the app should warn them if they probably won't be served before the registrar closes, but there is no place for that warning on this screen. (4) **Leave the queue** is a large button at the bottom, close to the thumb, so it could be tapped by accident and Loi would lose their place (error prevention).

**Change:** I will relabel #12 as `[ticket number]` and label "11 people are ahead of you" as `[position]`. I will mark "Your turn is near!" as a conditional alert that only shows when the turn is near, and highlight it when it does. I will add a small `[closing warning]` line under the wait time (for example, "You may not be served before the office closes"). I will add a confirmation step to **Leave the queue**   ("Leave the queue? You will lose your place."). I will also fix the main flow numbering, which starts at 3 and has a typo ("4 m"), so it reads 1 to 5.


## Staff dashboard (phone and laptop)

**Works well:** **Call Next** is the largest button and sits near the top on both the phone and the laptop, and Rina uses it the most, so it's the easiest to reach. This follows the rule about one click or tap per action. The counts per concern are at the top, so Rina can see what students need without extra navigation, and the laptop table shows the ticket, name, concern, status and actions in one view.

**Problem:** (1) After Rina presses **Call Next**, nothing on the screen shows who was just called, because every row still says "Waiting" (visibility of system status). (2) **Serve** and **No-show** appear on every row, including students who haven't been called yet, so Rina could serve the wrong person (error prevention), and the two buttons sit right next to each other. (3) A few labels are inconsistent: "No-show" on the phone vs "No show" on the laptop, "Change of Subjects" vs "Change of subjects", and the laptop has a select and a separate Filter button for one action (consistency).

**Change:** I will add a "Called" status that is highlighted (and moves the called student to the top), and only show **Serve** and **No-show** for the student who is called, with the rest showing no action buttons. I will make all labels consistent ("No-show", "Change of subjects") and fix the frame titles to "Staff dashboard". I'm keeping the table on the laptop and the cards on the phone, because the cards avoid sideways scrolling on a small screen.