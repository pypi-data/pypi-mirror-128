.. _man_datalad-x-snakemake:

datalad x-snakemake
===================

Synopsis
--------
::

  datalad x-snakemake [-h] [-d DATASET] [--version] ...


Description
-----------
Thin wrapper around SnakeMake to obtain file content prior processing

When snakemake is called through this wrapper, it is patched to use
DataLad to ensure that file content is obtained prior access by snakemake.
However, only content of files that are actually required for a particular
workflow execution will be obtained.


Options
-------
SNAKEMAKE ARGUMENTS
~~~~~~~~~~~~~~~~~~~
Start with '--' before any snakemake argument to ensure such arguments are not processed by DataLad.

**-h**, **--help**, **--help-np**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
show this help message. --help-np forcefully disables the use of a pager for displaying the help message

**-d** *DATASET*, **--dataset** *DATASET*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Constraints: Value must be a Dataset or a valid identifier of a Dataset (e.g. a path)

**--version**
~~~~~~~~~~~~~
show the module and its version which provides the command

Authors
-------
datalad is developed by Michael Hanke <michael.hanke@gmail.com>.
