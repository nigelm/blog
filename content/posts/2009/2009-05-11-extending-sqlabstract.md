---
author: nmether
date: 2009-05-11 19:48:28+00:00
draft: false
title: Extending SQL::Abstract
type: post
url: /2009/05/11/extending-sqlabstract/
categories:
- perl
---

Most of the perl I write currently has ties into
[DBIx::Class](http://search.cpan.org/perldoc?DBIx::Class) and hence uses
[SQL::Abstract](http://search.cpan.org/perldoc?SQL::Abstract).

I also have far too much of a preference for boolean items, which I normally
encode in the database as a column of type boolean (or the
[SQLite](http://sqlite.org/) vague equivalent).

Its been fairly easy to encode a test for boolean value being true with
SQL::Abstract - although the syntax

    
    column => \''


which maps to

    
    WHERE column


is a little esoteric.  However its downright close to impossible to produce
the opposite test without using literal SQL (actually the first version uses
literal SQL - except the SQL statement is NULL and comes _after_ the column
reference).

So today I have spent a little time extending SQL::Abstract to support the
-bool and -not_bool unary operators which allow both positive and negative
boolean tests to be encoded in a way that does not resort to literal SQL.

As part of this I refactored a part of SQL::Abstract so that further
extensions of this type can be added more easily - adding a unary_ops
extension to the constractor in the same way as the previously existing
special_ops.

So now:-

    
    -bool      => this_column,
    -not_bool  => that_column


will map to

    
    WHERE this_column AND NOT that_column


The code for this is currently sitting in a [svn
branch](http://dev.catalyst.perl.org/svnweb/bast/browse/SQL-Abstract/1.x/branches/bool_operator/)
- please have a look and comment on this.  My own criticism of it is that the
syntax is clunky, but we are restricted to the perl datastructure mapping
approach of the existing code (which is the real _raison d'etre_ of
SQL::Abstract).
