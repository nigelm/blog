---
author: nmether
date: 2009-06-03 19:52:01+00:00
draft: false
title: CPAN RPM  Packaging
type: post
url: /2009/06/03/cpan-rpm-packaging/
categories:
- perl
---

Seeing as I have been asked about building RPM packages of CPAN modules today
I thought it was worth putting some information down in a blog post - I would
love comments on this, so that I can improve the information and hopefully
make my processes better.

Firstly, I target Centos 4 and 5 i386 only, although I am going to have to
start building for x86_64 too) and build stuff for our own internal
requirements, the latter meaning that the stuff I package depends very much
one what I need for work at the time.  Its also a little painful that I cannot
easily make this work generally available, but getting these packages into the
wild would be complex.  Packaging for other RPM flavoured distros should be
easy enough, but slightly different.

There are a set of rules we work to for our internal deployments:-



1. Everything is packaged as RPMs.
2. You do not cheat on dependancies - if I do yum install foobar then foobar had better bring in all the appropriate required packages/modules
3. We have 3 repositories - the first 2 are the standard Centos repos (or rather local mirrors) of the base os and updates respositories.  The third is our own local repository of packages we build.  We require that all packages are signed so have our own internal GPG key for our repos.
4. All packages in our repository are built by us in a clean build environment and have no dependancies from outside the 3 repos we use.
5. Packages should pass their own test suite (which we run as part of the build) unless there are exceptional circumstances

Although, as I stated above, we are building things for our own internal use,
we do always contribute bug reports and fixes back to the upstream software
provider (unless the patch is only needed due to our own bad practice) -
maintenance is much easier if you keep close to upstream.

There are really 2 parts to building CPAN RPMs:-

1. Making a source RPM (or even just the spec file)
2. Building the binary RPMs

I'm going to consider these separately.


### Creating The Source RPM




<blockquote>_Mediocre Writers Borrow; Great Writers Steal_ - **T.S. Eliot**</blockquote>


Ideally use a source RPM package from a packager that you trust.  In my
experience the [Fedora](http://fedoraproject.org/) guys have now got the best
RPM packaging of perl modules - they have a set of [package
rules](https://fedoraproject.org/wiki/Packaging/Perl) they work to, and a good
set of tools.  If the Fedora folks have packaged a CPAN module then I will use
their source RPM in preference to building one myself.  If there are problems
with that RPM then I will contribute fixes back to their packagers (or the
upstream CPAN author).  The best place to check for packages is the
development sources directories - for example
[http://mirrors.kernel.org/fedora/development/source/SRPMS/](http://mirrors.kernel.org/fedora/development/source/SRPMS/)

Fedora also produce the [EPEL](https://fedoraproject.org/wiki/EPEL) (Extra
Packages for Enterprise Linux) additional packages for RHEL/Centos.  Generally
the only difference between these and the Fedora packages are possibly slight
changes of dependancies due to the different OS environment (and Fedora uses
perl 5.10 rather than Centos/RHEL perl 5.8).

If you can't find a prebuilt source RPM file you will need to create your own.
 Although this is a relatively simple task (but unfortunately one that always
appears to be hard to find documentation about) there are some additional
tools to do the heavy lifting for you - these at least produce the skeleton of
the package, but in many cases they produce a completely usable package with
no intervention required.

I used to use [cpan2rpm](http://perl.arix.com/cpan2rpm/) to produce packages -
the version I had was hacked around (not code I was proud of) to produce
better build dependancy listings.

However for the last couple of years I have been using
[cpanspec](http://cpanspec.sourceforge.net/) - another product of those
incredible [Fedora](http://fedoraproject.org/) packagers.  This produces a
completely usable RPM in the vast majority of cases.  A typical invocation
(for me) looks like:-

    
    $ cpanspec --follow --srpm SQL::Abstract


The follow flag does its best, but you do normally need to package
pre-requisites yourself before packaging the required package.

cpanspec is packaged within the [EPEL
repositories](https://fedoraproject.org/wiki/EPEL).


### Building RPMs


Basic information on building RPM packages can be found in the [RPM Building
Crash
Course](http://perso.b2b2c.ca/sarrazip/dev/rpm-building-crash-course.html), as
well as on the [rpm.org
wiki](http://www.rpm.org/wiki/Docs#PackagerDocumentation).

However it is best practice when building RPMs to build in a clean build
environment to ensure that all the dependancy generation is correct, that no
unpackaged files affect the build and to make sure the whole process is
reproducible.  This is done by having a separate chrooted build system that is
regenerated for each new build.

Until a couple of years back I used the
[mach](http://thomas.apestaart.org/projects/mach/) build system to produce
clean builds (there is a [HowTo
document](http://www.howtoforge.com/building-rpm-packages-in-a-chroot-environment-using-mach)
on this) - and I actually still use mach for building Centos 4 packages
(because the system hasn't broke so I've had no need to fix it).  However for
Centos 5 (and for any new environments) I now use
[mock](http://fedoraproject.org/wiki/Projects/Mock) (again from Fedora).

mock is packaged within the [EPEL
repositories](https://fedoraproject.org/wiki/EPEL).

In both cases you will need to configure your build system for the right base
OS and repositories.

If you are building significant numbers of packages you will need additional
scripting to manage things such as adding built packages to the repository
([createrepo](http://fedoraproject.org/wiki/Extras/CreateRepo)), expire off
superseded packages
([repomanage](http://skvidal.wordpress.com/2004/10/21/repomanage-among-other-things/))
and check that your repositories have no unfulfilled dependancies
(repoclosure) - these programmes are generally all in the yum or yum-utils
packages.
