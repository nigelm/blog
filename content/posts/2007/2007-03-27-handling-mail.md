---
author: nmether
date: 2007-03-27 11:28:00+00:00
draft: false
title: Handling Mail
type: post
url: /2007/03/27/handling-mail/
categories:
- email
- history
- mac
---

I pretty much live by email.  I've been using it for around 25 years now, and
have had good access to internet email for close on 20 years.  I've been on
open development mailing lists for all of that time, and have at times been
receiving  many hundreds (if not thousands) of messages a day.

I  obviously don't read all those messages - not in detail - and since I
maintain a bunch of machines that send all sorts of general notification mail,
much of it is glanced at (ie just look at sender and subject) and either
ignored or deleted.

All this mail means I have strategies in place to cope with it - for at least
15 years all my incoming mail has been sorted by incoming filters and dropped
into appropriate mailboxes.  List mail is filed in a folder for the list it
comes from, admin email is sorted into a few categories, expected commercial
mail is also sorted etc.  And that rarest of commodities, real personal mail,
hits my inbox (or one of the 4 inboxes I currently use).

During my period of using Email I have used
[elm](http://en.wikipedia.org/wiki/Elm_%28e-mail_client%29),
[NeXTMail](http://en.wikipedia.org/wiki/NeXTMail),
[MH](http://en.wikipedia.org/wiki/MH_Message_Handling_System),
[exmh](http://www.exmh.org/),
[evolution](http://en.wikipedia.org/wiki/Novell_Evolution) and finally
[Mail.app.](http://en.wikipedia.org/wiki/Mail_%28application%29)

I have to admit that I am really conflicted with Apple's Mail.  One the one
hand it does a lot of stuff really well (searching for example), and there are
some really neat extensions - for example
[MailTags](http://www.indev.ca/MailTags.html) is great.  But the foundations
seem a little shakey.

Somewhere deep in its heart, Mail is a basic
[POP](http://en.wikipedia.org/wiki/Post_Office_Protocol) client - it does
[IMAP](http://en.wikipedia.org/wiki/Internet_Message_Access_Protocol), but
even though it handles this to a higher standard than many mail clients, it
still isn't really happy with the concept of lots of folders which other
things can manipulate.

For example, the rules mechanisms seem to handle mail that was delivered
somewhere other than the Inbox poorly - sometimes they don't filter it,
sometimes they do.

Obviously for me, since 99% of my mail goes nowhere near my Inbox, this is a
problem.  And one I need to work on further...
