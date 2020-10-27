#!/usr/bin/env bash

if [ -z "${ATS_BASE}" ]; then
    echo "Please ensure environment variable ATS_BASE is set and run again..."
    exit 1;
fi
    
cd ${ATS_BASE}
mkdir -p modulefiles scripts amanzi ats amanzi-tpls/Downloads testing
#echo "# ------ begin code written by ats_manager/setup_ats_manager.sh ------"
#echo "export ATS_BASE=${ATS_BASE}" >> ~/.bash_profile
#echo "export PYTHONPATH=${PYTHONPATH}:${ATS_BASE}/ats_manager" >> ~/.bash_profile
#echo "module use -a ${ATS_BASE}/modulefiles" >> ~/.bash_profile
#echo "# ------ end code written by ats_manager/setup_ats_manager.sh --------"
