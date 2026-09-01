---
kind: walkthrough
axis: walkthrough
themes: [networking, identity]
platforms: [self-host]
marker: "mixed"
language: en
summary: "Walkthrough one: an empty floor plate, a hundred people, four segments, and how many radios end up in the ceiling — walked from the lift doors to the rack, deciding on the way."
counterpart: walkthrough/01-the-network.zh.md
sources: [the-reference-office.md, cross-cutting/site-network-design.md, build-out/05-network.md]
published:
---
# Walkthrough 01 · The network — one floor, four segments, and the radios in the ceiling

<!-- beat: arrive-empty-floor -->
The lift doors open onto an empty floor. No partitions, no carpet, the ceiling still hanging half-finished with the cable tray showing above it. There are some chalk marks on the slab from whoever looked at it last. The windows are big. The light is good. That is all there is.

<!-- beat: what-the-landlord-says -->
The agent standing in the doorway says it seats a hundred people.

<!-- beat: hundred-is-a-payroll-number -->
A hundred is a payroll number. It is not a number about this room. Those two have never been the same number, and almost every design that goes wrong starts by treating them as one.

<!-- beat: tuesday-is-sixty-five -->
Put enough buildings side by side and a very steady curve shows up. On the busiest midweek day, attendance runs in the mid sixties percent. Which means a hundred-person office, on a Tuesday, is a sixty-five-person office.

<!-- beat: monday-and-friday -->
Monday is low fifties. Friday is high thirties. Same floor, same people, same week.

<!-- beat: size-for-tuesday -->
So you size for Tuesday. Not for the payroll, and not for Friday.

<!-- beat: why-not-hundred -->
Size for a hundred and what you have bought is a space that sits half empty every day of the year, and you will pay rent on it for ten of them.

<!-- beat: why-not-friday -->
Size for Friday and Tuesday does not fit. And not fitting is something that happens once a week, every week, not occasionally.

<!-- beat: seventy-desks -->
Desks first. A desk per person stopped being the rule some time ago; hybrid offices provision somewhere between six and eight desks for every ten people. Take seven, and a hundred people means seventy desks. That seats a sixty-five-person peak comfortably and leaves a little room for the day it runs over.

<!-- beat: seven-rooms -->
Meeting rooms scale at roughly one per ten to twenty people. Where you land inside that range is not decided by headcount, it is decided by how open the floor is. A fully open floor pushes toward one per ten, because people with no door need somewhere to go. This floor is open. So, seven.

<!-- beat: the-mix -->
How you split those seven is where most offices get it wrong, and this one has actually been measured. Sensors across thirteen countries, a hundred and seventy-three buildings and more than twenty-seven thousand workspaces found that eight in ten meetings happen in rooms built for six or fewer.

<!-- beat: boardroom-empty -->
And the big room, the one that seats seventeen or more, sits at twelve percent utilisation. Four days out of five, it is a locked empty room.

<!-- beat: the-mix-answer -->
So: one large, two medium, four small. Roughly half the rooms seat two to four people.

<!-- beat: six-booths -->
Then six phone booths on top of that. They are not small meeting rooms. They solve a different problem — one person needs to take a call — and folding them into the meeting room count is the standard way a floor ends up with nowhere to take a call.

<!-- beat: now-the-network -->
Good. People, desks, rooms. All of them have numbers now. The network is next.

<!-- beat: the-instinct-is-to-buy -->
The instinct at this point is to ask what to buy. Whose switches, how many access points, which firewall. I would leave that question alone for a while, because it is the fifth question, not the first.

<!-- beat: four-questions -->
Strip every vendor away and a site network answers four things. And they come in an order.

<!-- beat: q1-who-talks-to-whom -->
One. Who is allowed to talk to whom. That is segmentation.

<!-- beat: q2-addresses -->
Two. What the addresses are, and what they will collide with. That is the address plan.

<!-- beat: q3-how-they-get-on -->
Three. How things get on. Wired ports, wireless, and what authenticates them.

<!-- beat: q4-who-answers-a-name -->
Four. Who answers a name and who hands out a lease. Which is to say, who owns DNS and DHCP.

<!-- beat: why-this-order -->
The order is not for tidiness. Each one constrains the next. You cannot write an address plan until you know what needs separating, and you cannot say where something lands until you know what the addresses look like.

<!-- beat: the-classic-failure -->
Get the order wrong and you get a very familiar result. The floor is addressed and cabled before anyone decides what should be separated. Segmentation becomes a retrofit. And a retrofit is the kind of work that goes on a plan and never comes off it.

<!-- beat: segment-per-trust -->
Segmentation first, and there is one rule. A segment per trust level, never a segment per device type.

<!-- beat: staff -->
The first is staff. That is the default one — authenticated humans and the managed devices in their hands.

<!-- beat: guest -->
The second is guest. Untrusted people, internet only, and the isolation has to be provable rather than assumed.

<!-- beat: unpatchable -->
The third one I tend to call the unpatchable. Door controllers, printers, the appliance in the meeting room, whatever is sitting on the lab bench.

<!-- beat: unpatchable-why -->
What they have in common is not that they are hardware. It is that they run vendor firmware, on a vendor's schedule, and they sit where anybody can walk up and reach them. Those three things together are why they get their own segment.

<!-- beat: management -->
The fourth is management. The management interfaces on the switches and the access points, reachable from exactly one place.

<!-- beat: four-is-right -->
Four is usually right.

<!-- beat: five-is-a-mistake -->
Five is usually a mistake.

<!-- beat: every-segment-is-a-rule-set -->
Because every extra segment is another rule set, and somebody has to stand up a year from now and explain why it looks the way it does. That somebody may not be you.

<!-- beat: the-tidy-argument -->
The extra segments almost always arrive carrying the word tidy. One per department. One per floor. One per kind of thing. And a tidy split produces exactly the rules that nobody can defend on the day they break something.

<!-- beat: the-real-test -->
So the test for a proposed segment is not, are these things different. The test is, what am I willing to block between them, and will I actually block it.

<!-- beat: a-vlan-is-not-a-boundary -->
A segment with an any-to-any rule back to the staff network is a VLAN, not a security boundary. Calling it a boundary is how an estate acquires a control that exists only on the diagram.

<!-- beat: before-the-first-subnet -->
The address plan. This gets written before the first subnet exists.

<!-- beat: write-against-what-breaks-it -->
And it gets written against the thing that will one day break it, which is: somewhere you will eventually have to tunnel to.

<!-- beat: non-overlapping -->
Every site, every branch, every VPN pool, every network in every cloud. None of them overlapping.

<!-- beat: checked-not-probably -->
Not probably fine. Checked.

<!-- beat: dont-pick-192-168 -->
And one more. Do not pick 192.168.0.0 or 192.168.1.0.

<!-- beat: why-not-192 -->
They work perfectly, right up until the day you need to reach them from somewhere that also chose them. Every home router and half the vendor appliances in the world ship defaulted into that space.

<!-- beat: size-for-the-lease -->
Size it for the growth in the lease, not for move-in day. This floor grows to about a hundred and thirty people without anyone moving.

<!-- beat: exactly-a-hundred -->
An address plan that fits exactly a hundred is a renumbering that has already been scheduled. Nobody has picked the date yet.

<!-- beat: leave-gaps -->
And leave gaps on purpose. Contiguous allocation looks tidy, and it makes the next segment impossible to summarise.

<!-- beat: summary-route -->
Allocate as though a summary route will one day matter, because on the day you add a second site, it does.

<!-- beat: the-merge -->
Here is what that rule is actually protecting you from. Two companies merge, or two estates have to reach each other, and both of them years ago picked out of the ten-dot space.

<!-- beat: three-options -->
From there you have three options. Renumber one side. NAT the overlap. Or proxy the whole thing at the application layer.

<!-- beat: all-three-are-projects -->
None of the three is an afternoon's work. All three are projects with names, budgets, and somebody assigned to them. Which is why the word checked earns the two hours it costs on day one.

<!-- beat: wireless-is-the-access-layer -->
Third question. How things get on.

<!-- beat: changes-what-wired-is-for -->
Wireless is the access layer now. That did not make wired go away. It changed what wired is for.

<!-- beat: aps-want-copper -->
The first thing that still wants a cable is the access point itself.

<!-- beat: aps-drive-the-switch -->
And this is the requirement that actually decides which switch you buy. Not the desk port count. Those few access point ports. A current access point wants a higher tier of power over ethernet and a two-and-a-half gigabit uplink.

<!-- beat: room-systems -->
The second is the screens and the room systems. A device carrying a meeting should not be competing for airtime, in that room, with every phone belonging to the people in the meeting.

<!-- beat: unpatchable-wants-cable -->
The third is printers, door controllers, everything sitting on that unpatchable segment. A cable is also a placement decision, and a wired port is far easier to pin to a VLAN than a wireless client is.

<!-- beat: desks-still -->
The fourth is desks. Still.

<!-- beat: not-because-people-use-them -->
But not because people use them. Most people will never plug in.

<!-- beat: cable-during-fitout -->
The reason is that pulling cable during a fit-out costs a rounding error, and pulling it afterwards is a project that lifts ceilings, clears floors, and needs a written method. Generous drops are cheap now and expensive later.

<!-- beat: is-it-still-gigabit -->
Somewhere around here somebody asks: is it still gigabit?

<!-- beat: three-answers -->
That question has three answers, because there are three tiers in this building and they move at different times, for different reasons.

<!-- beat: desk-least-starved -->
The desk port has almost nothing pushing on it. Hybrid moved the load to wireless and the storage to SaaS. The desk is the least starved link in the building.

<!-- beat: desk-upgrade-is-the-misread -->
Upgrading it first is the classic misread, and the most common way to spend the budget in the wrong ceiling.

<!-- beat: ap-uplink-moves -->
The tier that actually moves is the access point uplink.

<!-- beat: one-gig-makes-ap-the-bottleneck -->
A current access point can exceed a gigabit on its radios alone. Give it a gigabit port and you have turned that access point into the bottleneck it was bought to remove. Multi-gig earns its money here, and only here.

<!-- beat: aggregation-oversubscription -->
The third tier is aggregation and core, and what matters there is oversubscription. Every access switch uplink lands here, and this is where a design quietly gets capped.

<!-- beat: order-matters-more -->
The order matters more than the numbers. The instinct is to upgrade the tier people can see, and the tier people can see is the one that needs it least.

<!-- beat: uplink-is-uncounted -->
Uplink and stacking are where the under-specification lives, for a simple reason. Access port count is easy to count, so it is rarely wrong. The path from access to core appears on no port list at all, so nobody counts it.

<!-- beat: who-answers-a-name -->
Fourth question, and the shortest one. Who answers a name, and who hands out a lease.

<!-- beat: dns-dhcp-ownership -->
DNS and DHCP are not technically hard. What is hard is ownership. Who is responsible, and who gets woken up. That has never been a technical question, and it will arrive in your ticket queue dressed as one.

<!-- beat: network-auth-is-identity -->
And authentication. Authentication on a port is identity wearing a networking hat. It belongs to the identity story; it just turns up wearing the network's clothes.

<!-- beat: what-youll-see -->
Let me name a few things here, so that you can recognise where you are when you walk into an unfamiliar comms room.

<!-- beat: 802-1x-radius -->
The thing doing the authenticating on the port is 802.1X. Standing behind it, answering who is this, is usually RADIUS. And behind RADIUS sits your directory.

<!-- beat: lldp-dhcp-relay -->
LLDP is how switches announce themselves to each other. A DHCP relay is what carries a request across a segment to a server that is not on it.

<!-- beat: not-how-they-work -->
How any of them completes a handshake, what the frames look like — I am not going to cover.

<!-- beat: recognise-not-mechanism -->
Not because it does not matter. Because it is a different ability. Recognising where you are standing, and being able to say what the wire is doing at this instant, can be learned separately, and this walk only teaches the first one.

<!-- beat: guest-provable -->
And back to the guest network one last time. The isolation has to be provable. Clients isolated from each other, outbound only, and you should be able to demonstrate it, not point at it on a diagram.

<!-- beat: now-the-radios -->
Right. Look up. The ceiling.

<!-- beat: the-footing-change -->
Before I talk about radios, I want to change my footing.

<!-- beat: what-it-is -->
Everything so far — segments, addresses, who authenticates, which tier moves — is work I have actually done and then lived with for years afterwards. The wireless arithmetic coming next is not. It is read, cross-checked and worked through, out of published vendor engineering guidance, and I have checked it for internal consistency. But I have not designed an office wireless deployment and then lived with it for three years. Those two things do not weigh the same, so I would rather say it than let a confident tone paper over it.

<!-- beat: count-it-twice -->
The method itself is solid, and solid enough that it has barely moved across several generations of radio. Count it twice, take the larger, then check it against coverage.

<!-- beat: by-client-count -->
First count. By client.

<!-- beat: the-devices -->
Sixty-five people on the floor on a Tuesday, at roughly two devices each. Add seven room systems, the devices in six booths, a few printers, a few door controllers. About a hundred and forty-five associated devices.

<!-- beat: 145-over-50 -->
An access point in a dense space handles a hundred clients on paper, but you plan around twenty-five active per radio and about fifty per access point. That is an airtime fairness limit rather than a spec sheet one, which is exactly why it has barely moved in a decade. A hundred and forty-five over fifty is about three.

<!-- beat: by-throughput -->
Second count. By throughput.

<!-- beat: the-targets -->
Per client targets: video conferencing around one and a half megabits, high definition video around three, a voice call small enough to ignore. Size on the highest bitrate application, not the average one.

<!-- beat: throughput-answer -->
About forty percent of devices are active at peak. Fifty-eight devices at three megabits is around a hundred and seventy-four megabits. One access point covers that.

<!-- beat: take-larger -->
Three and one. Take the larger. Three.

<!-- beat: coverage-floor -->
Now check it against coverage. A partitioned office wants roughly one access point per two and a half to three thousand square feet. This floor is about eleven thousand.

<!-- beat: four -->
That gives four.

<!-- beat: the-surprise -->
Notice what just happened. What binds the number is coverage, not capacity.

<!-- beat: below-150 -->
That surprises people, because everything they have been told says density is what matters now. Density does decide it — above about a hundred and fifty people. Below that, the coverage floor usually wins.

<!-- beat: placement -->
Last step. Place them for the busiest square metre, not the average one. Uniform spacing serves a floor with meeting rooms in it worse than deliberate placement does.

<!-- beat: large-room-earns-a-radio -->
And the large room earns a radio of its own. It is the only square metre on this floor where twenty cameras come on at the same moment, and at that moment there are not twenty people in the corridor outside it.

<!-- beat: five-or-six -->
Add that in and you land on five or six.

<!-- beat: density-decides-where -->
So at this size, density decides where they go and coverage decides how many there are. Those two get collapsed into one sentence constantly, and once collapsed the sentence is no longer usable.

<!-- beat: now-down-to-the-rack -->
Last stop. Down to the rack.

<!-- beat: count-the-ports -->
Count the ports. Seventy desks. Seven rooms with a display and a room system each, fourteen. Six booths. Six access points. Three or so printers. Three or so door controllers and readers. Then eight for signage, spares, and the things nobody has thought of yet.

<!-- beat: 110-active -->
About a hundred and ten active ports.

<!-- beat: growth-135 -->
With growth to a hundred and thirty people, about a hundred and thirty-five. Three forty-eight port switches.

<!-- beat: poe-watts -->
But the thing that actually picks which switch is usually not the port count.

<!-- beat: 500w -->
It is the power budget. Six access points, plus the room and booth devices, plus door access, lands near five hundred watts of simultaneous draw.

<!-- beat: varies-by-two -->
And two switches with the same forty-eight ports can differ by more than a factor of two on power budget. Same port count, completely different set of things they can actually carry.

<!-- beat: specify-watts -->
So specify the watts. Not just the ports.

<!-- beat: uplink-stacking-again -->
And uplink and stacking. That is the second time today, because it is the one thing in all of this that is both load-bearing and will never raise its hand to remind you it exists.

<!-- beat: closing-what-bound -->
Look back at what bound each answer. The desk count was bound by Tuesday. The room mix was bound by those eight-in-ten meetings of six people or fewer. The radio count was bound by coverage, not capacity. The switch was bound by watts, not ports.

<!-- beat: closing-none-of-them -->
Not one of those four is the intuitive answer.

<!-- beat: closing -->
So next time you are standing in an empty floor plate, you can leave the buying question alone for a while. Ask who is allowed to talk to whom. Everything else lines up behind that one.
