---
kind: walkthrough
axis: walkthrough
themes: [incident, networking, observability]
platforms: []
marker: "mixed"
language: en
summary: "Walkthrough three: twelve minutes past nine on a Tuesday, and two people say the same sentence. The first ten minutes of an incident in a hundred-person office — which decisions are yours, which checks eliminate nothing, and why the fix is not the deliverable."
counterpart: walkthrough/03-the-day-it-breaks.zh.md
sources: [the-reference-office.md, build-out/01-uplink.md, cross-cutting/debug-ladder.md, cross-cutting/incident-response.md, cross-cutting/labs/remote-access-four-causes/README.md, cross-cutting/labs/mitigate-before-diagnose/README.md, the-stack/06-observability.md]
published:
---
# Walkthrough 03 · The day it breaks — the first ten minutes, and why the order matters

<!-- beat: tuesday-twelve-past-nine -->
It is twelve minutes past nine on a Tuesday. Tuesday is the busy day here. About sixty-five of the hundred people on payroll are in the building, which is most of the people this floor ever holds at once.

<!-- beat: somebody-walks-up -->
Somebody walks up to the service desk. They can do that without deciding to, because the desk sits on the walk from the lift to the seats, which is a choice somebody made on a plan, two walks back.

<!-- beat: the-sentence -->
What they say is one sentence. I cannot get in. It just says it cannot sign me in.

<!-- beat: a-second-person -->
Ninety seconds later a second person says the same sentence. Not a similar one. The same one.

<!-- beat: two-is-not-two -->
That is worth being careful about, because it is tempting to hear two reports and think you have two pieces of information. You have one piece of information, said twice.

<!-- beat: what-the-sentence-carries -->
And the sentence carries almost nothing. It tells you somebody tried and something refused, and it does not tell you which of the things in the chain refused, or whether the same thing refused both times.

<!-- beat: four-causes -->
Here is why that matters. Take remote access, the one place in this office where this exact sentence shows up most. Four completely unrelated faults produce it. A certificate on the gateway that expired over the weekend. An identity provider having a bad hour. A captive portal on a hotel network, intercepting. And a tunnel that installs a more specific route which does not happen to carry the traffic authentication uses.

<!-- beat: byte-identical -->
Four different incidents. Four different fixes. One report, word for word identical in all four. From where you are standing at the desk, the symptom is carrying zero diagnostic information.

<!-- beat: so-the-first-question -->
So the first question is not what is broken.

<!-- beat: it-is-what-is-it -->
The first question is what exactly is it.

<!-- beat: rung-zero -->
There is a rung below the first rung, and it costs nothing, and it is the one people skip. Three things, established and written down somewhere the ticket can see them.

<!-- beat: the-exact-name -->
The exact name or the exact address. Not the site. The name.

<!-- beat: from-which-machine -->
From which machine. Not from a person. From a machine, in a place, on a network.

<!-- beat: what-works-looks-like -->
And what working would look like. What would you see, if this were fine.

<!-- beat: sympathising -->
If you cannot state that third one, you are not debugging. You are sympathising.

<!-- beat: four-names -->
The reason this rung exists is dull and it is real. The thing the user calls the site has four names. Two of them are aliases. One of them resolves to something different inside this building than it does outside it.

<!-- beat: the-wrong-target -->
The most expensive hour in this job is the one spent climbing the whole ladder correctly, against the wrong target.

<!-- beat: look-up-from-the-desk -->
While that is being written down, look up.

<!-- beat: the-doors-open -->
The floor is fine. The doors open. The lights are on. The lift works. Somebody is making coffee.

<!-- beat: the-idf -->
And the room the first walkthrough took you into is fine too. Three access switches, a core, six radios in the ceiling, a controller. All of it up.

<!-- beat: nothing-here-is-broken -->
Nothing on this floor is broken. That is not a relief. That is the shape of the problem.

<!-- beat: the-old-answer -->
A decade ago a dead circuit meant no email and no internet, and the file server and the domain controller kept working in the next room. People were annoyed. People were not stopped.

<!-- beat: today -->
Today a dead circuit means nobody can log in. For an office whose work lives entirely off site, the uplink is the business.

<!-- beat: test-two -->
There is a question this office already asked itself, in a calmer moment, when it was deciding what deserved a place in that room. What has to keep working here on a day the uplink is down.

<!-- beat: the-honest-list -->
The honest list is short. Getting into the building. Getting out of it. And the fire panel.

<!-- beat: not-your-work -->
Everybody's work is in a tenant they cannot reach anyway. A company like this one does not need local continuity for its work. It needs it for its doors. That is a much smaller requirement than most arguments for keeping a server room assume.

<!-- beat: the-first-decision -->
Now, before anybody touches anything, there is a decision. It is the most consequential thing that happens in the first ten minutes and it is not a technical decision.

<!-- beat: mitigate-or-diagnose -->
Do you stop the bleeding first, or do you find out what is bleeding.

<!-- beat: the-slogan -->
Every version of this advice you have ever heard says mitigate first. Roll it back, fail it over, turn the thing off, put people on the other path. Then investigate.

<!-- beat: the-slogan-is-right -->
The slogan is right. It is also not unconditional, and the difference between knowing the slogan and knowing its conditions is most of what seniority is on this particular subject.

<!-- beat: nine-minutes -->
Measured against a realistic spread of causes, mitigating first saves about nine minutes of mean downtime. That is the win, and it is a real one.

<!-- beat: six-in-the-tail -->
It also costs about six minutes in the tail. The worst case gets worse.

<!-- beat: exactly-the-window -->
And the six is not mysterious. It is exactly the mitigation window. Six minutes spent attempting a generic fix on a cause that generic fix was never going to cover.

<!-- beat: the-worst-one -->
Which means the incident that costs you the extra six minutes is, by definition, one of the ones the mitigation could not help. The worst incident you will ever have is one of those.

<!-- beat: right-way-round -->
That trade is the right way round. You take a small, bounded, known cost on the rare incident in order to remove a large one from every common incident. Anybody who quotes you the nine minutes and not the six is selling.

<!-- beat: the-crossover -->
And it inverts. If the generic mitigation covers less than about forty percent of the plausible causes, diagnosing first is the better call. The advice is not a law. It is a bet on your own coverage.

<!-- beat: the-mitigation-that-hurts -->
There is a second condition, and it is the one that catches people. Some mitigations can make things worse. A failover that flaps. A rollback that corrupts. A restart that loses the queue. Once the expected damage from attempting the mitigation gets past about ten minutes, mitigating first is simply the wrong call.

<!-- beat: what-to-be-able-to-say -->
So the thing worth being able to say out loud is not the slogan. It is the two conditions under which the slogan stops being true. And notice what that means about the rehearsed failover and the tested restore elsewhere in this building. They are not insurance against the incident. They are what makes this instinct correct in the first place.

<!-- beat: now-the-ladder -->
Mitigation is running. Now you climb.

<!-- beat: five-rungs -->
Does the name resolve, and to what you think. Is there a route, and does the return path exist. Do the filters allow it, both layers, both directions. Do small packets work and big ones hang. And only then, may you look.

<!-- beat: each-cheaper -->
Each rung is cheaper than the one below it and eliminates more than the one below it. That is the entire design, and it is why skipping is expensive rather than untidy.

<!-- beat: the-rule -->
And there is one rule that decides whether something is a rung at all. A check earns its place by what it eliminates, not by what it reports.

<!-- beat: restart-the-client -->
Restart the client eliminates nothing. All four of those causes are still possible afterwards.

<!-- beat: is-the-tunnel-connected -->
Is the tunnel connected eliminates nothing either. Same four, still standing.

<!-- beat: they-feel-like-progress -->
They feel like progress because they produce a result. Producing a result and removing a possibility are different things, and only one of them is debugging.

<!-- beat: ping -->
This is also why one very famous command has no rung of its own.

<!-- beat: ping-eliminates-nothing -->
A ping that fails is consistent with a routing problem, a filter, a dead host, and a policy that simply drops it. It eliminates nothing. Which is not an argument against running it. It is an argument against believing it.

<!-- beat: refused-or-timed-out -->
One rung carries the highest information answer in this whole business, and the answer is a single word.

<!-- beat: refused -->
Refused means your packet arrived, and something at the far end actively said no. Routing works. Filtering to that host works. The problem is at the other end, and it is a service not listening or bound to the wrong interface. You just eliminated three rungs with one word.

<!-- beat: timed-out -->
Timed out means you know nothing. A dropped packet, a black holing filter, a wrong route and a dead host all look exactly like this, and there is no way to tell them apart from here.

<!-- beat: a-timeout-is-not-an-answer -->
A timeout is not an answer. It is the ladder telling you to keep climbing.

<!-- beat: the-mtu-rung -->
There is one rung people skip and then spend the rest of the day underneath.

<!-- beat: the-signature -->
The signature is unmistakable once you have seen it. The handshake completes and the transfer stalls. Logging in works. Downloading does not.

<!-- beat: the-boundary-names-the-tunnel -->
And a failure here tells you more than a fix would. The packet size where it breaks names the overhead, and the overhead names the encapsulation. The thing that is wrong announces which tunnel it is wearing.

<!-- beat: now-you-may-look -->
And now, four rungs later, you may open a capture.

<!-- beat: a-hobby -->
Not before. You arrive at the capture with a hypothesis, because four rungs eliminated the alternatives, and you open it to confirm or kill that hypothesis and then you stop. A capture opened without a hypothesis is a hobby.

<!-- beat: back-to-the-four -->
Go back to the four causes and the one sentence, and watch what the difference actually buys.

<!-- beat: elimination-solves-four -->
Checks chosen for what they rule out resolve all four. Every time. With a bounded worst case.

<!-- beat: habit-solves-two -->
Habit resolves two of the four. On the other two it spends the same number of checks and finishes unable to say which one it is.

<!-- beat: the-masquerade -->
And there is a trap in the middle of it. Asking whether you can reach the identity provider returns exactly the same answer whether the provider is genuinely down or a hotel captive portal is intercepting you. The check cannot tell those two apart.

<!-- beat: dns-separates-them -->
The one observation that does separate them is whether a name you already know resolves to the answer you already know.

<!-- beat: the-phase-trap -->
And the fourth cause fails after the word connected. The tunnel reports connected. Authentication still fails.

<!-- beat: worse-than-useless -->
Every check that asks whether it is up answers yes. Which makes the reflex check worse than useless on that one. It does not merely fail to help. It points away from the fault.

<!-- beat: footing-changes -->
Everything up to this point is ground the person telling you this has stood on. Ladders, tunnels, names that resolve differently indoors, the day the certificate expires over a weekend. What comes next is different footing, and it is worth saying so out loud rather than letting the voice stay level. The next part is the process around the outage, and it is mapped and verified rather than lived at scale.

<!-- beat: who-is-here -->
So. How many people are handling this.

<!-- beat: one-position -->
There is one walk-up service desk position on this floor. One. It sits on the circulation route, beside the store it draws spares from and beside the rack it is first responder for.

<!-- beat: fifty-hours -->
The support window is eight in the morning to six in the evening, Monday to Friday. That is fifty hours against a forty hour week, and it is the number that actually decides staffing, which is why it gets written down as a choice rather than absorbed as an assumption.

<!-- beat: forty-eight-tickets -->
And after the automation this office is supposed to build, the queue runs at about forty-eight tickets a week.

<!-- beat: more-hands -->
When something like this morning happens, the instinct is to add people to it.

<!-- beat: it-stops-paying -->
Responders do not add up linearly. Every one of them has to be told what is already known, and the telling comes out of the same minutes as the fixing. Model that and the curve flattens fast. Adding responders stops paying at about five.

<!-- beat: this-office-has-fewer -->
This office does not have five. It has one position and whoever else can be pulled off what they were doing.

<!-- beat: so-the-ic-is-a-hat -->
Which means incident commander here is not a role. It is a hat, and this morning it is probably on the same head as everything else.

<!-- beat: still-somebody-decides -->
The point of the role was never the ceremony. It is that somebody is deciding and somebody is recording. When it is one tired person, they are doing both, and knowing that is what stops the response from becoming a scramble that nobody can reconstruct afterwards.

<!-- beat: the-silent-responder -->
There is one failure mode worth naming because it is invisible from inside. Heads down, fixing, no updates. Leadership panics, piles on, and now the responder is answering questions instead of working. Still working, next update in fifteen. That sentence costs nothing and it buys the next fifteen minutes.

<!-- beat: the-record -->
And the record is not admin. A post-mortem is only ever as good as what somebody wrote down while it was happening, and nobody has ever reconstructed a timeline accurately from memory the following afternoon.

<!-- beat: while-that-happens -->
While that is going on, there is something else true about this floor that nobody is looking at.

<!-- beat: twenty-six -->
About twenty-six things on it will never tell you anything useful.

<!-- beat: what-they-are -->
Door controllers. Printers. The room systems. The booth devices. Vendor firmware, on the vendor's schedule, and no way to change either.

<!-- beat: they-answer-a-ping -->
You can see whether they answer. You cannot see what they are doing. And no purchase changes that, which is the part worth sitting with. The first limit on monitoring is not your tooling. It is the other end.

<!-- beat: the-second-limit -->
The second limit is worse, because it is invisible. You can only monitor what you know about.

<!-- beat: the-inventory -->
Coverage is always measured against an inventory. If the inventory is a subset of what exists, then the coverage percentage is a statement about the subset, and it is a true statement, and it is answering a smaller question than the one you asked.

<!-- beat: ninety-eight-percent -->
It will read as ninety-eight percent while the thing that broke this morning sits outside it.

<!-- beat: third-limit -->
Third. Every monitored thing costs a credential. An agent needs an identity, and that identity has no start date, no manager and no last day. At full coverage, the monitoring platform is the most privileged system in this building, and almost nobody designs it as though it were.

<!-- beat: fourth-limit -->
And fourth, coverage is not detection. You can collect everything and detect nothing. An alert nobody acts on is a dashboard.

<!-- beat: replace-the-objective -->
So replace the objective. Monitor everything cannot be achieved, and more usefully, it cannot be checked. There is no test that tells you that you got there.

<!-- beat: know-what-you-are-not -->
Knowing what you are not monitoring can be both. It turns coverage from an aspiration into a subtraction. This is the estate you can enumerate. This is the part of it that reports. And this list in between is where an incident will be slower, deliberately, and here is the reason for each line.

<!-- beat: at-three-in-the-morning -->
That list is the deliverable. It is also the only thing in this section that survives a change of tooling.

<!-- beat: it-comes-back -->
At some point this morning, it comes back. Somebody renews something, or a provider's status page goes green, and the floor stops looking up.

<!-- beat: the-fix-is-not-the-deliverable -->
The fix is not the deliverable.

<!-- beat: the-gap -->
Every incident's real deliverable is the gap it exposed, closed. The log line nobody was writing. The service nobody had instrumented. The alert that would have fired before anybody walked up to that desk.

<!-- beat: blameless -->
And the review is blameless, which is not a kindness and not a culture slogan. Blame makes people leave things out. Things left out make the next one worse. It is an operational requirement wearing a nice word.

<!-- beat: the-other-side-of-the-same-limit -->
There is one more thing to look at before the floor goes quiet, and it is the same limit as the monitoring one, arriving from the other side.

<!-- beat: five-places -->
Company information in this office lives in five places. The tenant. The endpoints. The directory. The records the IT function keeps about itself. And the services nobody listed.

<!-- beat: four-of-five -->
Four of those five can be given a recovery objective. The fifth cannot, and the reason is not budget or effort. You cannot set a recovery objective for a system you have not inventoried.

<!-- beat: same-limit -->
Which is the monitoring limit again, in different clothes. Both of them stop at the edge of the same list, and neither of them tells you where the edge is. Two of the most expensive guarantees this function makes, and they fail at the same place.

<!-- beat: once-a-year -->
This office performs one restore drill a year, and records that it did.

<!-- beat: not-paperwork -->
That drill is not paperwork. It is the only place in this entire building where we can recover stops being an opinion and becomes a thing somebody watched happen, on a date, with a duration attached.

<!-- beat: the-floor-fills-again -->
It is the afternoon now. The floor is full again. Sixty-five people, a hundred and forty-five devices in the air, seventy desks and somebody in a booth.

<!-- beat: nobody-remembers -->
In a month nobody in this building will remember how long this morning took.

<!-- beat: they-will-remember -->
What will still be true is which rung got skipped, and whether anybody wrote down why.

<!-- beat: count-the-minutes -->
The first walk counted the radios. The second counted the people twice, once for the desks and once for everyone who has ever held an account. This one counts the minutes.

<!-- beat: closing -->
And the only minutes worth defending are the ones somebody spent because they decided to. Every other minute this morning was spent because nobody had decided anything, and those are the ones that come back.
