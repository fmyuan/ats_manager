ATS Manager
===========

This is my own personal preference for how to set up managing multiple
ATS and Amanzi installations on a machine.

Requirements
------------

* git
* python3: note we highly recommend the
  [Anaconda3](https://www.anaconda.com/products/individual) package
  manager for your OS, and conda environments are provided here.
  Don't use your system python!

Recommended, though can be installed by us...

cmake
^^^^^

version >= 3.10ish?

* for mac: `brew install cmake`
* for ubuntu: `apt-get install cmake`

openmpi or another MPI installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* for mac: `brew install openmpi`
* for ubuntu: `apt-get install libopenmpi-dev`

**Be sure to set `MPI_DIR` to the install location.  This can be found by inspecting the results of `mpicc -show` for the location of the library.**

* for mac: `export MPI_DIR=/usr/local/Cellar/openmpi/VERSION`
* for ubuntu: `export MPI_DIR=/usr/lib/x86_64-linux-gnu/openmpi` or similar

**Place this in your `.bashrc`

blas and lapack
^^^^^^^^^^^^^^^

* for mac: commandline tools? provides the Acclerate framework
* for ubuntu: `apt-get install libatlas-base-dev`
  
environment modules
^^^^^^^^^^^^^^^^^^^

* for mac: `brew install modules`  NOTE: you likely have to follow instructions after running this to activate it.  Something like `echo ". /usr/local/modules/Modules/init/bash" >> ~/.bashrc` will do it.

* for ubuntu: `apt-get install environment-modules`  NOTE: Again, you likely have to do something to activate it.  Something like `echo ". /usr/share/modules/init/bash" >> ~/.bashrc` will do it, or (globally) `sudo ln -s /usr/share/modules/init/bash /etc/profile.d/modules.sh`


Installation
------------

Note this is installation of _this_ package, not of ATS or Amanzi.  That comes next...

Decide where to put ATS, download this repo, and run the setup script.

    export ATS_BASE=~/code/ats
    mkdir -p ${ATS_BASE}
    git clone https://github.com/ecoon/ats_manager.git ${ATS_BASE}/ats_manager
    . ${ATS_BASE}/ats_manager/setup_ats_manager.sh


Usage
-----

Scripts provided here make it fairly easy to clone, configure, install, run, and test Amanzi and ATS installations of multiple branches.


Set up an existing branch of Amanzi or ATS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**TBD**

Create a new branch and run setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**TBD**

Pull and update an existing Amanzi and/or ATS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**TBD**

Run Amanzi unittests
^^^^^^^^^^^^^^^^^^^^

**TBD**

Run ATS regression tests
^^^^^^^^^^^^^^^^^^^^^^^^

**TBD**
