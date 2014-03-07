# Sumatra Demonstration

## Authors

 * [Daniel Wheeler](http://wd15.github.io/about.html)

## Overview

This repository provides notebooks for demonstrating the use of
[Sumatra](http://neuralensemble.org/sumatra/).

## License

The repository is licensed with the FreeBSD License, see
[LICENSE.txt](LICENSE.txt).

## Requirements

The [REQUIREMENTS.txt](REQUIREMENTS.txt) file has a complete list of
packages in the Python environment during development. The most
important of these are listed. The version numbers are mostly not
important within reason, but if you have problems the version numbers
may help.

 * Sumatra: `3c00d7cc`
 * GitPython: 0.3.2.RC1
 * FiPy: `08d564f9`
 * IPython: 2.0.0-dev
 * Matplotlib: 1.3.1
 * Numpy: 1.7.1
 * PySparse: `1751931a`
 * Trilinos: 11.4.3
 * PyTrilinos: 4.10d
 * Pandas: 0.12.0
 * Django: 1.5.5
 
## Sumatra Hacks

The following hack was made to the Sumatra version `3c00d7cc`.

    diff -r 3c00d7ccfbd1 sumatra/launch.py
    --- a/sumatra/launch.py	Mon Jul 15 17:30:39 2013 -0400
    +++ b/sumatra/launch.py	Fri Mar 07 14:59:17 2014 -0500
    @@ -191,8 +191,8 @@
         generalised in future releases.
         """

    -    def __init__(self, n=1, mpirun="mpiexec", hosts=[], options=None,
    -                 pfi_path="/usr/local/bin/pfi.py", working_directory=None):
    +    def __init__(self, n=1, mpirun="mpirun", hosts=[], options=None,
    +                 pfi_path="/home/wd15/anaconda/bin/pfi.py", working_directory=None):
             """
             `n` - the number of hosts to run on.
             `mpirun` - the path to the mpirun or mpiexec executable. If a full path
    @@ -257,10 +257,11 @@
             try:
                 import mpi4py.MPI
                 MPI = mpi4py.MPI
    +            raise ImportError
             except ImportError:
                 MPI = None
                 warnings.warn("mpi4py is not available, so Sumatra is not able to obtain platform information for remote nodes.")
    -            platform_information = LaunchMode.get_platform_information()
    +            platform_information = super(DistributedLaunchMode, self).get_platform_information()
             if MPI:
                 import sys
                 comm = MPI.COMM_SELF.Spawn(sys.executable,
    @@ -293,7 +294,7 @@
         (https://computing.llnl.gov/linux/slurm/)
         """

    -    def __init__(self, n=1, mpirun="mpiexec", working_directory=None, options=None):
    +    def __init__(self, n=1, mpirun="mpirun", working_directory=None, options=None):
             """
             `n` - the number of hosts to run on.
             `mpirun` - the path to the mpirun or mpiexec executable. If a full path
    @@ -341,7 +342,6 @@
             else:
                 cmd += " %s %s %s %s" % (executable.path, mpi_options,
                                          executable.options, arguments)
    -        print cmd
             return cmd
         generate_command.__doc__ = LaunchMode.generate_command.__doc__


## Viewing the Notebooks

The Notebooks can be viewed at
[nbviewer.ipython.org](http://nbviewer.ipython.org/github/wd15/smt-demo/tree/master/)
and are automatically updated as changes are pushed to the repository.

