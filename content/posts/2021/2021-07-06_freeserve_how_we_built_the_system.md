---
title: "Freeserve - How We Built The System"
date: 2021-07-06T00:00:00+01:00
categories:
  - Blog
  - 2020
tags:
  - Freeserve
  - ISP
  - History
---
> “Success has many fathers, but failure is an orphan”

There have been many people who have claimed to be "The Inventor of
Freeserve", although in many cases it appears the more fuss they make about
this title the less they had to do with it...  I wasn't in the room when that
particular proposal was made (although I have quite strong suspicions on who
originally proposed the idea), but I was on the original implementation team
within Planet Online.

I mostly worked in the Core Systems group at Planet between 1995 and 1999.  As
part of that I worked on the CAG (Connect and Go) systems which provided a
white label dial up ISP service for the likes of `Prestel`, `Kingston` (the
Hull telecoms provider) and `Channel 6` which was a predecessor to Freeserve.

And then I worked on Freeserve.  In particular the sign up and authentication
system were mine, as well as the mail system.  However this particular
reminiscence is going to concentrate on the mail systems.

## What Was Freeserve

[Freeserve](https://en.wikipedia.org/wiki/Freeserve) was a consumer ISP
originally run by Dixons (the high street tech chain) with Planet Online.
Dixons gave a huge advertising and high-street footprint - they had a store
on every UK high street where you could pick up your Freeserve floppy disk or
CD.

Although Freeserve was not the very first to offer no-fee dial-up internet
service, the clout of Dixons and the advertising campaign meant that it took
off at a rate of knots, putting on 900,000 accounts in the first 4 months
after its launch in 1998.

The service initially ran over dial-up modems, using a national dial up number
which was free of charge to the initiator.  Through the magic of the
complicated UK telephony cross-charging system this provided a small
termination payment to the service provider - and this was used to pay for the
service.  There were other revenue streams - advertising, premium technical
support and later pay for services.

## Why Now?

I was talking to a couple of friends this morning, and Freeserve was
mentioned.  My friend was incredibly enthusiastic about the Freeserve mail
system - how you could set up different email addresses within the domain and
have a set of filtering to individual family mailboxes - in 1998!  And I had
to say "I wrote that".

Last year was 25 years since we started Planet Online - I was one of the first
3 hires there.  But, and especially with the Covid situation, that anniversary
passed unnoticed.  Its 22 years since Freeserve launched and made a
significant change to the UK home internet market - in the last couple of
years the last vestiges of the Freeserve name and service have been finally
closed off.

## Freeserve Email

Freeserve email addresses were of the form `user@example.freeserve.co.uk` -
the `user` part could be anything, and it was just the
`example.freeserve.co.uk` part that identify the Freeserve account.
All messages to any user `@example.freeserve.co.uk` would end up in one
single POP3 mailbox.

As was normal for the time, email was provided to the customer over POP-3,
with outgoing email sent by SMTP via a Freeserve mail server.  To reduce SPAM
and other shenanigans there was a route map applied to the Freeserve
terminating modem racks which forced all SMTP connections to a local (to the
modem rack) SMTP server.

The mail receiving stack was [Exim](http://www.exim.org/) delivering into a
[Maildir](https://en.wikipedia.org/wiki/Maildir) mail spool which resided on a
set of NetApp NFS filesystems.  This gave us a huge (for the era), mail spool
with fairly high availability.  There were some performance tweaks applied to
make this work for the size of mail spool and loading.

The [Maildir+](https://en.wikipedia.org/wiki/Maildir) specification allows
additional tag information to be added to a message by tweaking the filename
that the message is saved under.  The configuration used saved both the
message size and the local recipient address into these tags.

The mail spool was NFS exported to a number of the mail servers - which were
all Linux systems.  The pop side was the [qmail](https://cr.yp.to/qmail.html)
`qmail-pop3d` with some local modifications and an additionally modified
`qmail-popup` using a locally built authentication utility to replace
`checkpassword`.

The `checkpassword` replacement queried the Freeserve RADIUS servers for
authentication.  Those had some additional performance tweaks which I may come
to another day.

The `qmail-popup` program collected the pop3 username and password.  The
username would be the email domain - ie `example.freeserve.co.uk` - however
you could also specify an email address - ie `user@example.freeserve.co.uk` -
and some other patterns.  These resulted in additional information being put
into the environment so that this data was available to the `qmail-pop3d`
later on.  Authentication was passed onto the `checkpassword` binary.

The main part of the POP daemon was  `qmail-pop3d` - this had several
modifications:-

- The size of each email is taken from the tag part of a Maildir message
  filename - this saved an additional stat() operation to check the mail
  size, which meant that for a NetApp filer all the information needed to
  produce a POP LIST was in the NetApp fast data.
- There was support for a broadcast email setup where previously unseen
  messages in a global mailbox are linked into the users own email.  Not
  sure if this was ever used but it allowed a space efficient way to send
  an email to all.
- The additional environment information from `qmail-popup` was used to
  filter the view of the mailbox - so if this had been set to `user` then
  only emails sent to `user@...` would be shown in the POP3 listings.
  This also used the additional information put into the Maildir+ tags
  to avoid having to read or stat the individual message files.

## Performance Tweaks

As described above, the pop daemon was tweaked to only stat or touch mail
files when absolutely necessary - basically when a message was actually read
by the client (after which the status would be updated by renaming - thats
Maildir semantics).

The Mail directory was hashed to spread the layout across the filer - this
could have been extended across multiple filer heads, but that was not
necessary during the time I was there. 

The mail hosts always attempted once to deliver external mail.  After that
they passed the mail to a fallback routing host which dealt with all the
things that could not be delivered immediately.  This kept control of the
size of the mail queues on eveerything except the fallback host (which had
different queue running parameters on it).

## Security Tweaks

Exim was running entirely as a single user, no setuid etc, this reduced the
possibilities for security exploits (although this also meant that Exim could
see the entire mail spool - but that was a relatively low risk problem at
that time).

The qmail side chrooted to the mail spool for a user on authentication.

Due to expected (and seen) issues with spamming (from our users), and
attempting to remain a good internet citizen, Freeserve blocked SMTP from end
users out of the network.  Even more so (and controversially), we routed all
SMTP connections to a local (to the modem rack pop) SMTP server.  This routed
all outgoing mail. It also had a view on all mail passing through it, and
used some very simple heuristics to pick up spam attempts - any SMTP
connection that attempted to push more than a few messages out would have the
mail queued for later checking.  This checking had more context on what was
happening outside the single mail connection, so could pick up mail bombing
runs (there was a craze for "Yo Momma" emails in the first months of
Freeserve).

The small number of people who hit the abuse filters had their mail blocked,
and after a small number of repeat offences had their username block and
their calling line ID (which we always received because it was required for
the telephony call class) was blocked.

After initial hysteria from the previously established large ISPs they did
grudgingly recognize that Freeserve was not a bad spam source.

## Notes

Originally I wrote this back in January, but hadn't quite finished it... and
then the post lingered for 6 months.  So I have now hurridly finished it off
and pushed it out because improving it further might mean it could wait
another 6 months...
