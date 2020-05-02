---
author: nmether
date: 2007-03-31 09:27:00+00:00
draft: false
title: Virtualisation
type: post
url: /2007/03/31/virtualisation/
categories:
- vm
- vmware
- xen
---

I've been looking at virtualisation recently - both for use within my group and for wider use with the company.

We need to be able to handle Windows VMs as well as proper operating systems,
so unfortunately things like [Open VZ](http://openvz.org/) or its commercial
cousin [Virtuozzo](http://www.swsoft.com/en/virtuozzo) are not an option,
which pretty much leaves Xen (both the Linux distribution hosted version and
the Xensource packaged version) and [VMWare.](http://www.vmware.com/)  Live
migration of VMs would be useful, although for its overkill for our group
requirements (but having it means we can test how things work in a clustered
environment with migration, so its down as a really want if not a must have).



The Xensource packaged Xen versions - we're evaluating [Xen
Enterprise](http://www.xensource.com/products/xen_enterprise/index.html) - are
interesting but appear a little early in their development at present, and
have poor SAN/storage options and no current live migration support.  VMWare
is the most flexible, polished and capable - its also by far the most
expensive.  Xen running under a Linux distribution (intention is to use
[Centos](http://www.centos.org/) 5) has yet to be tested.


More work to see what else is good needs to be done here....
