#!/usr/bin/env bash

# ensure we are in ATS_SYSTEM_BASE
if [ `pwd` -ef ${ATS_SYSTEM_BASE} ]; then
    echo "Executing from ${ATS_SYSTEM_BASE}..."
else
    echo "Please execute this from ${ATS_SYSTEM_BASE}"
    exit 1;    
fi

# ensure one argument, the branchname
if [ "$#" -ne 1 ]; then
    echo "Usage: branch-ats.sh BRANCHNAME"
    exit 1;
fi

# ensure not existing branch
if [ -d ats/repos/dev-$1 ]; then
    echo "Repo: dev-$1 already exists."
    exit 1;
fi

# make a module file
echo "Copying modulefile: modulefiles/ats/dev to modulefiles/ats/dev-$1"
cp modulefiles/ats/dev modulefiles/ats/dev-$1
echo "gsed -i 's/atsname dev/atsname dev-$1/g' modulefiles/ats/dev-$1"
gsed -i "s/atsname dev/atsname dev-$1/g" modulefiles/ats/dev-$1

# load the module
module purge
module load ats/dev-$1
module list

# clone the ATS_SRC_DIR
echo "Cloning ATS into new repo..."
cd ats/repos/
git clone dev dev-$1

if [ -d dev-$1/.git ]; then
    cd dev-$1
    echo "Branching..."
    git checkout -b dev-$1
else
    echo "...Unable to clone git repo?"
    cd ${ATS_SYSTEM_BASE}
    exit 1;
fi

cd ${ATS_SYSTEM_BASE}

# configure ats
echo "Configure/build/install ATS..."
. config-files/configure-ats.sh
cd ${ATS_SYSTEM_BASE}


echo "...done"
exit 0;
