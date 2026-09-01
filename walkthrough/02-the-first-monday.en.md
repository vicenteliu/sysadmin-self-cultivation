---
kind: walkthrough
axis: walkthrough
themes: [identity, endpoint]
platforms: [m365]
marker: "mixed"
language: en
summary: "Walkthrough two: one person arrives on a Monday, and everything they need was decided the week before. What it takes to seat one joiner, twenty-three times a year — and the two things in this office that no event ever triggers."
counterpart: walkthrough/02-the-first-monday.zh.md
sources: [the-reference-office.md, build-out/03-identity.md, build-out/04-devices-and-images.md, build-out/15-joiner-mover-leaver.md]
published:
---
# Walkthrough 02 · The first Monday — one joiner, and the two things nothing ever triggers

<!-- beat: monday-ten-to-nine -->
It is ten to nine on a Monday, and there is somebody standing in the lift lobby who has never been here before.

<!-- beat: floor-is-not-empty -->
The floor behind them is not the one from the first walk. The partitions are up, the ceiling is closed, the cable tray is out of sight where it belongs. Seventy desks, seven meeting rooms, six booths. Somebody is already making coffee.

<!-- beat: one-of-twenty-three -->
This person is not special. They are one of about twenty-three people who will do exactly this in the next twelve months.

<!-- beat: what-they-need -->
Four things have to be true before they can sit down and work. An account that says who they are. A machine. A way onto the network. And a seat on whatever this company uses to get anything done.

<!-- beat: none-of-it-happens-today -->
None of those four gets built today. Every one of them had to be true before the lift doors opened.

<!-- beat: monday-is-a-test -->
Monday does not build anything. Monday reveals what was built. That is the whole reason this walk is worth taking.

<!-- beat: the-trigger-question -->
So go back. Something, somewhere, decided that this person exists. What was it?

<!-- beat: not-a-ticket -->
If the answer is that a manager filed a ticket, stop. Everything downstream of that answer is going to be late, incomplete, or both, and no amount of automation further along will fix it.

<!-- beat: the-real-question -->
The question worth asking is narrower and much harder. What system decides whether a person is still an employee?

<!-- beat: one-system-decides -->
There has to be one. Not two that mostly agree. One, named, that everything else believes.

<!-- beat: usually-hr -->
Usually it is whatever HR runs, because that is where the start date and the last day actually live. It is rarely the system anybody wants it to be, and it is almost never the directory.

<!-- beat: the-account-is-easy -->
Given that trigger, the account is the easy half. A name, a mailbox, a password nobody has yet used.

<!-- beat: the-groups-are-hard -->
What they can reach is the hard half, and it is decided by one rule that sounds like pedantry until the second year.

<!-- beat: the-group-rule -->
A group means a job function, or a group means an access bundle. Never both.

<!-- beat: why-the-rule -->
Because the moment a group means both, it cannot be changed for one reason without changing the other. Move somebody between teams and their access moves with them, silently, in a direction nobody chose.

<!-- beat: automation-is-faithful -->
And automation is faithful. It applies the model exactly as written. If the model confuses those two things, the automation propagates the confusion at machine speed, to every new hire, consistently.

<!-- beat: consistent-is-worse -->
Consistent is worse than sporadic here. A sporadic mess gets noticed. A consistent one becomes the way things are done.

<!-- beat: eight-functions -->
This office has eight functions. Finance, sales, engineering, and five more. Eight is a small number. It is small enough that nobody thinks a group model is worth designing, and large enough that the wrong one takes years to unwind.

<!-- beat: the-device-was-ordered -->
Somewhere in the same week, a laptop was ordered.

<!-- beat: where-the-image-lives -->
The interesting part is where its image lives, and the answer today is: not in this building. Nobody here builds it. The vendor registers the machine to this company before it ships, and on first boot it reaches out and pulls its own policy.

<!-- beat: what-that-replaced -->
That replaced a task-sequence server, a technician, and thirty to sixty minutes per machine. It only works if the identity work was done first. If it was not, this is not zero-touch. It is a re-imaging project wearing zero-touch as a costume.

<!-- beat: the-box-arrived -->
The box itself arrived on Thursday and went into the store, which is the room with a door that locks, sitting next to the rack.

<!-- beat: store-is-a-shelf -->
The store is not big. It holds about five spare machines, the returns that have not been wiped yet, and whatever is in transit. Five sounds thin until you work out what it is for.

<!-- beat: what-five-covers -->
Five covers the joiners arriving before the next order lands, which is about two a month, and the machines that die in that same month, which is a fraction of one. It is a lead-time number, not a stock policy.

<!-- beat: ten-services -->
And then the seats. This office can name about ten services it owns. A directory, a productivity tenant, file storage, device management, endpoint security, backup, remote access, a ticket system, conferencing, and something watching all of it.

<!-- beat: and-one-more -->
Our joiner also needs a seat on at least one thing that is not on that list, because somebody in their team bought it on a card eighteen months ago and never told anyone.

<!-- beat: hold-that-thought -->
Hold onto that one. It comes back at the end, and it is the most expensive sentence in this walk.

<!-- beat: back-to-the-lobby -->
Back to the lobby. Ten to nine.

<!-- beat: walk-past-the-desk -->
The walk from the lift to their desk goes past the service desk, and that is not an accident. It sits on the circulation route, visible from the floor, near the store it draws stock from and near the rack it is first responder for.

<!-- beat: why-placement-matters -->
Put that same position in a back office and something specific happens. The walk-ups become tickets. Nobody decided to change the workload. Somebody moved a desk.

<!-- beat: their-desk -->
Their desk is one of seventy, in a floor built for sixty-five people on a Tuesday. There is a chair. There is a monitor. There is a machine that has never been switched on.

<!-- beat: first-boot -->
First boot. It asks who they are.

<!-- beat: not-what-it-is -->
Note what it does not ask. It does not ask what the machine is, or where it is, or which cable it is attached to. It asks who is holding it.

<!-- beat: the-network-asks-the-same -->
And when it reaches the network, the network asks the same question. That is 802.1X, and behind it RADIUS, and behind RADIUS the same directory that issued the account.

<!-- beat: the-port-does-not-decide -->
The port does not decide anything. You could carry this machine to any desk on this floor, or into any of the seven meeting rooms, and it would land in the same place.

<!-- beat: which-segment -->
Which is the staff segment, because they authenticated. There are four segments on this floor and that is the one for people who proved who they are.

<!-- beat: the-other-three -->
The other three are guest, unpatchable, and management.

<!-- beat: guest-has-no-register -->
Guest is worth a sentence, because it is the only one with no register at all. You do not enrol a visitor. You size that segment by the peak day and let it be untrusted, and being untrusted on purpose is what makes it safe.

<!-- beat: by-lunchtime -->
By lunchtime our joiner is working. Mail, files, chat, the tool their team lives in. Nobody walked them through a setup wizard.

<!-- beat: how-many-tickets -->
So how many tickets did today generate? If all of it was built properly, close to none.

<!-- beat: fifty-three-and-sixty-two -->
Here is that number from two directions. The support model says enrolment and imaging generate about fifty-three tickets a year once zero-touch is built. The fleet arithmetic says the office hands over about sixty-two machines a year, counting refresh and joiners together.

<!-- beat: seven-for-eight -->
Seven tickets for every eight handovers. Most machines change hands and nobody files anything at all, and some do not, and that gap is what a working provisioning path looks like from the outside.

<!-- beat: two-derivations -->
Those two numbers were derived from completely different things. One from ticket rates, one from a refresh cycle. They describe the same office and they agree, which is the only kind of confirmation this sort of planning can offer.

<!-- beat: now-do-it-again -->
Now do all of that twenty-three times.

<!-- beat: and-seventeen-out -->
And about seventeen times in the other direction, because people leave.

<!-- beat: footing-changes-here -->
This is where the footing under this walk changes, and it is worth saying out loud rather than letting it slide past.

<!-- beat: what-is-borrowed -->
The turnover figure is borrowed. A rate in the middle teens is the band professional-services and technology employers usually sit in, and that band comes from published employer figures, not from anybody here having run this company's payroll.

<!-- beat: what-is-not-borrowed -->
What is not borrowed is the structure. Joiners equal leavers plus growth. That sentence is arithmetic and it does not care what the turnover rate is.

<!-- beat: move-the-band -->
So move the band. Take it down to one in ten and every number after this changes. The shape of the argument does not move at all, and the shape is the part worth carrying to your own building.

<!-- beat: forty-events -->
At the middle of that band it comes to about forty joiner-and-leaver events a year. One about every six working days.

<!-- beat: every-six-days -->
Not a project. Not a season. Every six working days, for as long as the lease runs.

<!-- beat: five-years -->
The lease runs five years.

<!-- beat: a-hundred-and-sixteen -->
Across it this office hires about a hundred and sixteen people.

<!-- beat: to-grow-by-thirty -->
In order to grow by thirty.

<!-- beat: two-hundred-and-sixteen -->
Add the hundred who were already here on day one, and roughly two hundred and sixteen different people hold an account in this company at some point.

<!-- beat: for-a-floor-of-one-thirty -->
For a floor that never holds more than a hundred and thirty of them at once.

<!-- beat: the-directory-is-not-the-office -->
Which means the directory is not the office. It is about one and seven tenths of the office, and that ratio only grows.

<!-- beat: snapshot-and-history -->
An office is a snapshot. A register is a history. Every estate IT administers is the second kind, and every intuition people have about size is the first kind.

<!-- beat: devices-do-the-same -->
The machines do exactly the same thing. About two hundred and twenty bought across the lease, to hold about a hundred and fifteen at a time.

<!-- beat: back-to-the-person -->
Now go forward three years and find the person from Monday morning.

<!-- beat: they-moved -->
They are still here. They changed teams eighteen months ago.

<!-- beat: a-joiner-has -->
Think about what each of the three lifecycle events actually gives you to work with. A joiner has a start date.

<!-- beat: a-leaver-has -->
A leaver has a last day.

<!-- beat: a-mover-has -->
A mover has a conversation.

<!-- beat: no-event-fires -->
No event fires. Nothing arrives in a queue. There is no date on which somebody is required to look, and so the move is handled the way conversations are handled, which is by granting what is now needed.

<!-- beat: mover-that-only-adds -->
And not removing what is not. Everybody builds it this way. It looks finished, because joiners work and leavers work.

<!-- beat: two-years-later -->
Two years and a few internal transfers later, the people who have been here longest have the most access in the company, and not one of them can tell you why.

<!-- beat: nobody-was-careless -->
Nobody was careless. Every individual grant was correct on the day it was made. The failure is that the leg with no trigger never got one.

<!-- beat: that-is-one -->
That is one thing in this office that nothing ever triggers. Here is the other, and it is larger.

<!-- beat: forty-identities -->
Count the identities in this building that are not people. There are about forty.

<!-- beat: what-they-are -->
Twenty-six of them are device credentials, because the network authenticates everything and the door controllers, the printers, the room systems and the booth devices all have to answer for themselves. About a dozen are service integrations between the ten named services. Two are break-glass accounts.

<!-- beat: two-in-five -->
Two identities in every five in this office are not a person.

<!-- beat: none-has-a-start-date -->
Not one of the forty has a start date.

<!-- beat: none-has-a-manager -->
Not one of them has a manager.

<!-- beat: none-has-a-last-day -->
And not one of them has a last day.

<!-- beat: the-door-controller -->
Think about the door controller. A leaver forces a review of one person's access, because a date arrives and a process starts. Nothing at all forces a review of a door controller's credential. It was issued during the fit-out and it will still be there when the lease ends.

<!-- beat: the-privileged-exception -->
The three privileged administrator accounts are the exception that proves the rule. They do expire, eventually, because the human behind each one eventually leaves.

<!-- beat: the-tail-service -->
And now the sentence from earlier comes back. The tool somebody bought on a card.

<!-- beat: no-leaver-reaches-it -->
When our joiner eventually leaves, the leaver process will revoke their seats on the ten services this company can name. It will not touch that one, because no leaver event reaches a service nobody wrote down.

<!-- beat: not-a-percentage -->
That is not a reclamation rate that could be improved. It is not ninety percent, or eighty. There is no process there at all.

<!-- beat: eighty-six-departures -->
Across one lease, eighty-six people leave this company. For anything outside the named ten, nobody revokes anything, because nobody with a revocation duty knows the tool exists.

<!-- beat: the-queue-knows -->
There is a place where all of this becomes visible, and it is the ticket queue.

<!-- beat: the-automation-works -->
Build the automation the sixteen steps ask for. Self-service password reset, zero-touch devices, automated joiner-mover-leaver. It works. It removes about two fifths of the ticket volume.

<!-- beat: what-does-not-move -->
One category does not move at all. Access and permissions. Afterwards it is the largest thing left in the queue, more than a third of everything.

<!-- beat: not-a-gap -->
That is not a gap in the automation. It is the estate arriving in the queue.

<!-- beat: what-generates-it -->
Access requests are produced by an identity population that is two fifths non-human with no lifecycle, against a service estate whose size this company does not know, over a register that changes about a hundred and twenty-three times a year.

<!-- beat: automating-a-path -->
Automating the request path does not shrink any of that. It just makes the same requests arrive faster.

<!-- beat: what-automation-removes -->
Look at which categories the sixteen steps do remove. Password resets. Enrolment. Joiner and leaver runs. Every one of them is a question with a deterministic answer.

<!-- beat: what-survives -->
And the one that survives is the one that ends with a person deciding whether somebody should be allowed to have something. That is the same boundary every step of the build-out arrives at when it asks what AI can be trusted with.

<!-- beat: monday-again -->
Next Monday there will be another one of these. Somebody in the lobby at ten to nine who has never been here before.

<!-- beat: the-floor-empties -->
This floor empties every Friday and fills again on Tuesday. Sixty-five people, a hundred and forty-five devices in the air, seventy desks, and by the high thirties on a Friday afternoon almost nobody.

<!-- beat: the-estate-does-not -->
The estate does not empty. It has never once, in the life of this lease, been smaller than it was the day before.

<!-- beat: closing -->
So when you are working out what a hundred-person office needs, count the people twice. Once for the desks, the radios and the rooms, which is what the building asks for. And once for everyone who has ever held an account, which is what you are actually administering.
