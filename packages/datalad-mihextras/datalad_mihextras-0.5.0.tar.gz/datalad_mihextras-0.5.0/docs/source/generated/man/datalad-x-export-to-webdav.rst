.. _man_datalad-x-export-to-webdav:

datalad x-export-to-webdav
==========================

Synopsis
--------
::

  datalad x-export-to-webdav [-h] [--url URL] [--mode {auto|verify}] [-d DATASET] [-r] [-R LEVELS] [--version] NAME


Description
-----------
Export a dataset to a WEBDAV server

WEBDAV is standard HTTP protocol extension for placing files on a server
that is supported by a number of commericial storage services (e.g.
4shared.com, box.com), but also instances of cloud-storage solutions like
Nextcloud or ownCloud. This command is a frontend for git-annex's export
functionality that can synchronize a remote WEBDAV target with a particular
state of a local dataset. It does not expose all of git-annex's
capabilities, such as transparent encryption, but aims to facilitate the
use case of sharing the latest saved state of a (nested) dataset with
non-DataLad users via a common WEBDAV-enabled storage service.

For the initial export, only a name for the export WEBDAV target (e.g.
'myowncloud') and a URL for the WEBDAV server are required.  An optional
path component of the URL will determine the placement of the export in the
directory hierarchy on the server. For example,
'https://webdav.example.com/datasets/one' will place the root of the
dataset export in directory 'datasets/one' on the server. It is recommended
to place datasets into dedicated subdirectories on the server.

Subsequent exports do not require a re-specification of a URL, the given
name is sufficient. In case only a single WEBDAV export is configured,
no parameter is needed at all.

When exporting recursively, subdatasets exports are placed at their
corresponding locations on the WEBDAV server. Matching export
configurations are generated automatically based on the superdataset's
configuration.

NOTE
  This command needs git-annex 8.20210312 (or later).

SEEALSO

  https://git-annex.branchable.com/git-annex-export
    Documentation on git-annex export

*Examples*

Export a single dataset to 4shared.com::

   % datalad x-export-to-webdav 4shared --url https://webdav.4shared.com/myds

Recursively export nested datasets into a single directory tree in a
box.com account::

   % datalad x-export-to-webdav box -r --url https://dav.box.com/dav/myds




Options
-------
NAME
~~~~
name of the WEBDAV service. Constraints: value must be a string

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**--url** URL
~~~~~~~~~~~~~
url of the WEBDAV service. Constraints: value must be a string

**--mode** {auto|verify}
~~~~~~~~~~~~~~~~~~~~~~~~
on repeated exports, git-annex relies on local knowledge which content was previously exported, and will only upload changes ('auto'); when content was modified independently at the export site this can lead to omissions, and a verification of file existence can be perform prior export ('verify') as a mitigation (this verification is not able to detect remote content changes). Constraints: value must be one of ('auto', 'verify') [Default: 'auto']

**-d** *DATASET*, **--dataset** *DATASET*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
specify the dataset to export. Constraints: Value must be a Dataset or a valid identifier of a Dataset (e.g. a path)

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
