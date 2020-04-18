---
author: nmether
date: 2009-06-01 20:56:05+00:00
draft: false
title: XML Processing
type: post
url: /2009/06/01/xml-processing/
categories:
- perl
---

Recently I have had to revisit one of our systems that deal with XML call records (from a VOIP switch).

This system splits out Call Detail Records (CDRs) by customer.  The version of this that was running was based on XML::Twig which used to run acceptably fast (this code was written a number of years ago), and has the advantage of being relatively light on memory as the document was processed a chunk at a time rather than being completely read into memory.   However the system was getting apparently slower - mainly down the volume of calls being detailed increasing by a substantial factor.

So last week I spent a while trying out different approaches to this problem (as well as investigating approaches for a more database driven storage system for the future).

For the specific problem of splitting the data based on the customer responsible for the CDRs, the fastest approach I managed to put together was based on XML::LibXML.  This has the disadvantage that it has to read in the complete XML file (and these are getting to be multi-gigabyte per hour), however the module is relatively light on memory compared to the other methods and a simplified rewrite of my previous programme resulted in a better than factor 20 speed up - rather worth having.

However this was basically a simple filter - splitting data coming in into several output streams based on a very simple criteria.  Getting data fields out of the XML records with XML::LibXML appears to be relatively slow (and clumsy) - so for example if I want to extract all the fields into a database then the aggregate cost of accessing all the fields starts to be costly.

XML::Bare converts XML data files into perl hashes - either its own format which includes metadata to aid in reconstruction to XML, or a basic hash format very very similar to that used by the more ancient XML::Simple.  Its fairly fast, although appears to be rather more profligate with memory (for some reason it holds the complete XML file as a string as well as hashified version - it also reads the whole file at once).  XML::Bare is pretty fast, and if you are doing a lot of manipulation of the data within the XML file it might well be faster than using XML::LibXML

The big advantage of using XML::Twig originally was that its a quite perlish method of manipulating XML, and additionally you can use the simplify operation to convert the XML data into a hash - useful for dealing with individual records within the XML set.

However this cannot be done with XML::LibXML, and XML::Bare is too inflexible.  So what would be useful was a fast mechanism for converting an XML::LibXML node into a hash making access within that node much simpler (and quite likely quicker - although there is an initial cost of conversion to a hash, as well as the memory cost).

I'm hoping to be able to set aside a little time to look at this.  However I guess people may tell me other approaches - unfortunately the documentation within the various XML modules is somewhat opaque so its quite likely I have missed a great big feature somewhere!
