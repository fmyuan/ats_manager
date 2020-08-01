ATS Deployment
==============

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

Decide where to put ATS, and add it to your shell init script, and clone this repo:

    export ATS_BASE=~/code/ats
    echo "export ATS_BASE=${ATS_BASE}" >> ~/.bashrc
    echo "module use -a ${ATS_BASE}/modulefiles" >> ~/.bashrc
    mkdir -p ${ATS_BASE}
    rmdir ${ATS_BASE}
    git clone https://github.com/ecoon/ats_setup.git ${ATS_BASE}
    cd ${ATS_BASE}

Configure
---------

Setup of this package is controlled in the file `bin/config.sh`.  Feel free to edit this file!


Usage
-----

Scripts provided here make it fairly easy to clone, configure, install, run, and test Amanzi and ATS installations of multiple branches.


Set up an existing branch of Amanzi or ATS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the scripts, `scripts/setup_existing_ats.sh` or `scripts/setup_existing_amanzi.sh`.


To clone, configure, and build an existing branch of ATS (here we assume master for both Amanzi and ATS):

    . bin/setup_existing_ats.sh --ats=master --amanzi=master --ats-regression-tests=master --disable-geochemistry

Note that this will use an existing repo if possible -- so for instance, if you already have isntalled Amanzi at master, and want to use that Amanzi and TPLs with ATS branch `dev/subgrid`:

    . bin/setup_existing_ats.sh --ats=dev/subgrid --amanzi=master

will do the right thing.  If you would like to re-install Amanzi and TPLs:

    . bin/setup_existing_ats.sh --ats=dev/subgrid --amanzi=master --clobber-amanzi --clobber-tpls

Similarly, for Amanzi:

    . bin/setup_existing_amanzi.sh --amanzi=master


Pull and update an existing Amanzi and/or ATS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This pulls new changes to an existing installation and rebuilds.  Note that all repos default to master:

    . bin/update_ats.sh master
    . bin/update_amanzi.sh master

Note the slightly different syntax.  As these already exist, master here refers not to the branch, but to the modulefile name.  These should almost always be the same as the ATS branch (in the case of `update_ats.sh` or the Amanzi branch (respectively).


Create a new branch and run setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Scripts are also provided to set up a new branch for development.  Always do this.  Don't do development in an existing branch, unless it is your branch that you started elsewhere.

    . bin/setup_new_ats.sh --amanzi=master --ats=ecoon/new_stuff
    . bin/setup_new_ats.sh --amanzi=ecoon/new_stuff --ats=ecoon/new_stuff
    . bin/setup_new_amanzi.sh --amanzi=ecoon/new_stuff



Run Amanzi unittests
^^^^^^^^^^^^^^^^^^^^

This assumes Amanzi has been installed, and you want to run unittests:

    . bin/run_amanzi_unittests.sh master


Run ATS regression tests
^^^^^^^^^^^^^^^^^^^^^^^^

This assumes ATS has been installed, and you want to run regression tests:

    . bin/run_ats_tests.sh master

