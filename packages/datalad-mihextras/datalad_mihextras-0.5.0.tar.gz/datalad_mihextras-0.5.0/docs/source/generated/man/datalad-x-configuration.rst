.. _man_datalad-x-configuration:

datalad x-configuration
=======================

Synopsis
--------
::

  datalad x-configuration [-h] [--scope {global|local|branch}] [-d DATASET] [-r] [-R LEVELS] [--version] [{dump|get|set|unset}] [name[=value] ...]


Description
-----------
Get and set dataset, dataset-clone-local, or global configuration

This command works similar to git-config, but some features are not
supported (e.g., modifying system configuration), while other features
are not available in git-config (e.g., multi-configuration queries).

Query and modification of three distinct configuration scopes is
supported:

- 'branch': the persistent configuration in .datalad/config of a dataset
  branch
- 'local': a dataset clone's Git repository configuration in .git/config
- 'global': non-dataset-specific configuration (usually in $USER/.gitconfig)

Modifications of the persistent 'branch' configuration will not be saved
by this command, but have to be committed with a subsequent SAVE
call.

Rules of precedence regarding different configuration scopes are the same
as in Git, with two exceptions: 1) environment variables can be used to
override any datalad configuration, and have precedence over any other
configuration scope (see below). 2) the 'branch' scope is considered in
addition to the standard git configuration scopes. Its content has lower
precedence than Git configuration scopes, but it is committed to a branch,
hence can be used to ship (default and branch-specific) configuration with
a dataset.

Any DATALAD_* environment variable is also mapped to a configuration item.
Their values take precedence over any other specification. In variable
names '_' encodes a '.' in the configuration name, and '__' encodes a '-',
such that 'DATALAD_SOME__VAR' is mapped to 'datalad.some-var'.

Recursive operation is supported for querying and modifying configuration
across a hierarchy of datasets.

*Examples*

Dump the effective configuration, including an annotation for common
items::

   % datalad configuration

Query two configuration items::

   % datalad configuration get user.name user.email

Recursively set configuration in all (sub)dataset repositories::

   % datalad configuration -r set my.config=value

Modify the persistent branch configuration (changes are not committed)::

   % datalad configuration --scope branch set my.config=value




Options
-------
{dump|get|set|unset}
~~~~~~~~~~~~~~~~~~~~
which action to perform. Constraints: value must be one of ('dump', 'get', 'set', 'unset') [Default: 'dump']

name[=value]
~~~~~~~~~~~~
configuration name (for actions 'get' and 'unset'), or name/value pair (for action 'set').

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**--scope** {global|local|branch}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
scope for getting or setting configuration. If no scope is declared for a query, all configuration sources (including overrides via environment variables) are considered according to the normal rules of precedence. For action 'get' only 'branch' and 'local' (with include 'global' here) are supported. For action 'dump', a scope selection is ignored and all scopes are considered. Constraints: value must be one of ('global', 'local', 'branch')

**-d** *DATASET*, **--dataset** *DATASET*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
specify the dataset to query or to configure. Constraints: Value must be a Dataset or a valid identifier of a Dataset (e.g. a path)

**-r**, **--recursive**
~~~~~~~~~~~~~~~~~~~~~~~
if set, recurse into potential subdataset.

**-R** LEVELS, **--recursion-limit** LEVELS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
limit recursion into subdataset to the given number of levels. Constraints: value must be convertible to type 'int'

**--version**
~~~~~~~~~~~~~
show the module and its version which provides the command

Authors
-------
datalad is developed by Michael Hanke <michael.hanke@gmail.com>.
