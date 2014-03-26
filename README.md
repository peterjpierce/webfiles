# webfiles

Deliver reports or other static content via HTTP in a simple but
attractive tabular interface that relies on file system conventions to
organize and style the presentation.

Provides:
+ Protected delivery (content behind logins)
+ Segregated catalogs for multiple recipient groups
+ Configurable mappings to infer and display:
  - Friendly report names
  - Revisions
  - Effective ("as of") dates

## Infrastructure

This is a WSGI application and provides directives to tweak and integrate
with Apache web servers using the Include option.  It is implemented using
Flask running under Python 3.

It does not require a database and expects to be run on UNIX-like OSes like
Linux, FreeBSD or OS X.

## Interim Note

This project is under development; this README will be fleshed out soon.
