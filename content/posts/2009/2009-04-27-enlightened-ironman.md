---
author: nmether
date: 2009-04-27 12:37:11+00:00
draft: false
title: Enlightened Ironman?
type: post
url: /2009/04/27/enlightened-ironman/
categories:
- perl
- theatre
---

Following the [blog
post](http://www.shadowcat.co.uk/blog/matt-s-trout/iron-man/) and
[proposal](http://www.enlightenedperl.org/ironman.html) from [Matt
Trout](http://www.shadowcat.co.uk/blog/matt-s-trout/), I'm going to aim to
push out some posts on my uses and experiences of perl.  I'm extraordinarily
unlikely to hit the Ironman rating since a look back at my history shows the
occaisional year between posts :-)

Anyhow, as an ancient perl user (I pulled a perl release from usenet back
sometime around 1988/89), I have quite a lot of odds of perl around, although
mostly I have been pretty good at retiring the stuff that has outstayed its
useful life.  In recent years there have been 2 main threads of work I have
been doing with perl:-



1. Stuff related to my day job - mostly a combination of glue code and some
   overall product management code.
2. Theatre back office applications - ie
   [website](http://jrtheatre.co.uk/) management and backstage
   allocation/management.

The 2 sets of code actually share a considerable amount of ideas - I tend to
take more risks with the theatre code, and often pull ideas from there into
work code.  However in both cases there is core of stuff that is based around
`DBIx::Class` and to a lesser extent `Catalyst`.

The next few posts are going to outline the theatre code in particular - what
the requirements were and how I went about implementing them.  There is a
degree of history there - its been an incremental addition of functionality
over several years, and if I were starting from scratch I may well not end up
with the same system now, but it works and I am reasonably happy with it
(although I have plans to improve it further as time allows).
