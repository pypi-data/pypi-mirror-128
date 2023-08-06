.. _man_datalad-x-export-bagit:

datalad x-export-bagit
======================

Synopsis
--------
::

  datalad x-export-bagit [-h] [--archive {tar|tgz|bz2|zip}] [-d DATASET] [-r] [-R LEVELS] [--version] PATH


Description
-----------
Export a dataset to a Bag-it

This is a proof-of-principle implementation that can export a DataLad
dataset into a BagIt bag, a standardized storage and and transfer
format for arbitrary digital content.

TODOs:

- Support bag-of-bags
  https://github.com/fair-research/bdbag/tree/master/examples/bagofbags
- Support for hardlinking local files into the bag so save space and time
  on export
- Support for automatically missing content on export
- Support for bag metadata specification

SEEALSO

   `RFC8493 <https://www.rfc-editor.org/rfc/rfc8493.html>`_
      BagIt specification.

*Examples*




Options
-------
PATH
~~~~
location to export to. With --archive this is the base path, and a filename extension will be appended to it. Constraints: value must be a string

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**--archive** {tar|tgz|bz2|zip}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
export bag as a single-file archive in the given format. Constraints: value must be one of ('tar', 'tgz', 'bz2', 'zip')

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
