---
author: nmether
date: 2009-05-03 21:24:39+00:00
draft: false
title: Theatre Management with Perl - 1
type: post
url: /2009/05/03/theatre-management-with-perl-1/
categories:
- perl
- theatre
---

First some history - in fact this post is almost all history and setting the scene for what we did later.

When I joined the theatre there was a website - however it had been done by someone's friend, and was a flash only movie containing information on the shows that were coming in the near future.  This suffered massively from being done in spare time and could take months to get updated, so something had to be done.

The first aim was to get a website that we could get event information onto with as little ongoing maintenance as I could get away with.   Unfortunatly the event information we did have was in Excel spreadsheets - and this was arranged in colour coded tabular form (one column per month, one cell per day) which was likely to be hard to parse automagically.

I decided the easiest way to handle the event information was to use an Excel spreadsheet - this would allow other members of the theatre technical team to update the events too.  Each event (which can cover several performance dates) had a single line, with several fields describing it.

A piece of perl (yup, we have finally got there), parsed out the events ([Spreadsheet::ParseExcel](http://search.cpan.org/perldoc?Spreadsheet::ParseExcel)) and built a set of per-month event pages as well as a front page with current events on it - using [HTML::Template](http://search.cpan.org/perldoc?HTML::Template).

The page generation was done off-line and the generated html pushed to the webserver - at that time we had to take this approach as the web server was separate to the machines with the appropriate tools to generate stuff.

As a fairly quick and dirty hack this worked extremely well - so much so that it stayed in place for more than 18 months - you can see examples of this on the way back machine - ie this one from [March 2004](http://web.archive.org/web/20050309090453/http://www.jrtheatre.co.uk/).  Meanwhile we were starting to wake up to the idea of having an events database - even one as primative as the one we had - and realising we could start to use this for our internal backstage management.

We had started to use a wiki for much of the backstage management - we have half a dozen stage managers plus other crew, all volunteers and organising all of us is not an easy task.  The wiki chosen was [MoinMoin](http://moinmo.in/) - at that time I could not see any perl wikis that I was happy with.  The wiki contained another list of events - this time in a way more focused on periods the theatre was booked (which is different to performance dates - it includes rehearsals and some events that have no performances such as training events).

So we were duplicating information - and I was updating a lot of that information I felt this was very much a bad thing.

So I started looking at producing a proper database and bringing a lot of this information together....
