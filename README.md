# Abusor

Abusor is a tool for managing network abuse data. It is designed to contain
all kinds of network abuse events (f.i. malware, hack attempts, etc), and will
try to aggregate related events into larger contexts (Cases). The rules that 
decide which network context is applied is configurable in the form of
Business Rules.

## Abusor flow example

For example, an Event is registered describing a spam email, sent from ip 
192.0.2.34. A Case is created for the Event. The event will also be assigned
a score.

Then another Event from the same ip is registered (another spam email?). The
new Event will be linked to the existing Case. The total score for the Case
will now go up. If the total score of the case goes up high enough, this
could result in an action like adding the ip to a blocklist.

When a third Event is registered and linked, the Case will be updated to
cover the whole 192.0.2.0/24 network block in stead of only the original ip.
All previously known Cases that apply to this network block are merged into
one Case. This again influences the total Case score.

More events can expand the Case netmask even more. After the /24 block, we
could expand to the /16 block, then up to the network block size that was
assigned by the LIR, or even to the ASN (all network blocks administered
by the same party).

Over time, the score for an Event will decrease: older events will weigh less 
on the total score. When the score of the Case drops below a certain
threshold, the Case will be closed. Of course, when new Events continue to be
added to the Case, the score won't drop enough to close the Case.

## Business rules

In the above example, all kinds of decision points can be configured:

* How high will the score be for an Event?
* When will the netmask for a Case be expanded? After X Events? When total
  score exceeds Y?
* When will a Case result in an action? Which action?
* How fast (over time) will Event scores degrade? What is the threshold for 
  closing a case?

## Registering events

The application has a simple that you can use for adding new events. A simple
commandline client is available in the `clients` directory. It's also possible
to manage Events and Cases manually through the API frontend, or through the 
admin interface.
