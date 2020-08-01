#!/usr/bin/env bash

if [ -z "$ATS_BASE" ]; do
    echo "Please ensure environment variable ATS_BASE is set and run again..."
    exit 1;
done
    
cd $ATS_BASE

mkdir -P modulefiles scripts amanzi ats amanzi-tpls/Downloads testing
git clone https://github.com/ecoon/ats_manager.git ats_manager
echo "export PYTHONPATH=${PYTHONPATH}:${ATS_BASE}/ats_manager" >> ~/.bash_profile

