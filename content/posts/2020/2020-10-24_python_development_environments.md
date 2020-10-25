---
title: "Python Development Environments"
date: 2020-10-24T17:47:31+01:00
---

I have spent a substantial number of years mostly programming in
[Perl](https://www.perl.org/), but this year I have been working on a team
that has a strong preference for [Python](https://www.python.org/) and so I
have converted across.

Previously I have dabbled in Python - I could read basic python, and had
patched various things - mainly [Ansible](https://www.ansible.com/) - in the
past, but had not done any serious work in the language.

However its not the transfer to the language thats caused most of the
headaches, but other things surrounding that - for example:-

- Development environment
- Formatting, checking, rules for how things go into git
- Documentation

We don't have much in the way of stated rules for these, and despite Python
being much more about there being one right way to do things, in terms of
overall development environments it all appears that there is a huge variety
of ways that people do stuff...

So this is what I am now moving to for things I am working on...


## Development Environment

I use [Poetry](https://python-poetry.org/).  This brings together management
of virtual environments, dependency lists etc as well as distribution builds
and pushing of packages to pypi or to a local repository.

The downside is that you tend to have to run things by `poetry run cmd...`,
but I mostly set that up in a Makefile to deal with that.   Additionally at
present the cost of running builds and deploys in CI is bloated by the
additional time to install poetry - I may build myself an appropriate Docker
image to ameliorate that.

The Makefile I add is hand crafted - mostly cargo-culted from that last thing
I did - but I now use the [self documenting Makefile
trick](https://www.freecodecamp.org/news/self-documenting-makefile/) to add a
set of help to the Makefile.

Version number handling is managed by
[bump2version](https://github.com/c4urself/bump2version) - using that to
rewrite the poetry version tag as well as updating the information within the
package `__init__.py` file (yes this may well be superfluous but the
alternatives appear to require loading additional modules just to find your
own version number).  Additionally I found a hack this last week to make
`bump2version` update the `CHANGELOG.md` file by using the alternate methods
of Markdown formatting (otherwise the `#` header markers cause the
`bump2version` config file to ignore the lines as a comment).

So in '.bumpversion.cfg' you have:-

```ini
[bumpversion:file:CHANGELOG.md]
search = <!-- insertion marker -->
replace = <!-- insertion marker -->
        [{new_version}] - {now:%Y-%m-%d}
        --------------------
```

and in `CHANGELOG.md` you have:-

```markdown
Unreleased Changes
------------------

<!-- insertion marker -->
- last commit changelog entry
```

## Pre-Commit Formatting / Checking

I have a `.pre-commit-config.yaml` file in each repository - mostly exactly
the same, but with some per-project tweaks.  I run
[`pre-commit`](https://pre-commit.com/) prior to each commit - mostly not
currently enforced by actually adding it to git hooks, although I may change
that as I did previously have a set of hooks set up by
[git-hooks](https://github.com/git-hooks/git-hooks) to run the perl
[TidyAll](https://metacpan.org/release/Code-TidyAll)

A sample `.pre-commit-config.yaml` file can be found
[here](https://github.com/nigelm/ssh2_parse_key/blob/master/.pre-commit-config.yaml),
but in general I am running a set of checks including the [black
formatter](https://github.com/psf/black), flake8 and mypy.

In terms of git management I currently tend to work in
[Fork](https://git-fork.com/) having previously used
[Tower](https://www.git-tower.com/) for many years (Tower is likely a bit more
powerful and slick, but it now costs more per year than Fork does outright -
although I hope that Fork will not regret going for a one off cost model).

## Documentation

Documentation is another thing that seems odd regarding python - there is the
start of a standard workflow defined with docstrings etc, and then things go a
bit freestyle.  I have to say I am not very keen on reStructuredText, and
Sphinx felt opaque to me - and then you hit several different API
documentation mechanisms, many of which appear to be machine rather than human
readable.  This is one of the areas where the Perl simple but consistant
documentation setup works better - although the python side does pull more
introspection information out of the code.

So I have settled on one I like (so far - only been working in this for a few
weeks) and that appears to work well with my other tools.

I use [MkDocs](https://www.mkdocs.org/).  With that I have been using the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.
Stacked on top of that are the
[`mkdocs-click`](https://github.com/DataDog/mkdocs-click) extension for CLI
tools, and [`mkdocstrings`](https://github.com/pawamoy/mkdocstrings) for API
documentation.

There is one little problem with the pipeline above in that `mkdocs-click` and
`mkdocstrings` use different function signature markup - this is something I
mean to have a look at in the future.

## CI etc

The CI workflow varies not least because I release some things on
[Github](https://github.com) using [Travis CI](https://travis-ci.org/), and
other things are handled by an internal [GitLab](https://about.gitlab.com/)
instance using GitLab CI.  However in both cases I have got a fairly standard
test, release and build documentation workflow with the artifacts going to the
appropriate repo and documentation going to Github/GitLab Pages.

I am not currently doing a lot of additional multi-version testing with `tox` etc.  I may move to this later, but am trying to take this a step at a time.
