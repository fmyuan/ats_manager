#!/bin/sh -f

source ~/.bash_profile

echo `which mpirun`
echo `which gcc`

# master with amanzi-TPLs to be built. 
# NOTE: --skip-clone is for using already cloned codes, otherwise with option --clobber
#       
python ./bin/install_ats.py \
       --machine cades-baseline --compiler-id openblas-0.3.23-openmpi-4.0.4-gcc-12.2.0 \
       --modulefile cmake/3.26.3 --modulefile python/3.11-anaconda3 --modulefile gcc/12.2.0 --modulefile openmpi/4.0.4 --modulefile openblas/0.3.23 \
       --skip-clone \
       --amanzi-branch master --ats-branch master --enable-geochemistry --build-type opt --tpls-build-type opt --trilinos-build-type opt \
        tpls-0.98.11 master

# master using already-built amanzi-TPLs
#python ./bin/install_ats.py \
#	--machine cades-baseline --compiler-id openblas-0.3.23-openmpi-4.0.4-gcc-12.2.0 \
#        --modulefile cmake/3.26.3 --modulefile python/3.11-anaconda3 --modulefile gcc/12.2.0 --modulefile openmpi/4.0.4 --modulefile openblas/0.3.23 \
#        --skip-clone \
#	--amanzi-branch master --ats-branch master --enable-geochemistry --bootstrap-options=--enable-elm_ats_api --build-type debug --tpls-build-type opt --trilinos-build-type opt \
#        --tpls tpls-0.98.11 \
#	tpls-0.98.11 master_elmatsapi


# specific branch
#python ./bin/install_ats.py \
#	--machine cades-baseline --compiler-id openblas-0.3.23-openmpi-4.0.4-gcc-12.2.0 \
#        --modulefile cmake/3.26.3 --modulefile python/3.11-anaconda3 --modulefile gcc/12.2.0 --modulefile openmpi/4.0.4 --modulefile openblas/0.3.23 \
#        --skip-clone \
#	--amanzi-branch master --ats-branch phongle/optimize_transport --enable-geochemistry --build-type opt --tpls-build-type opt --trilinos-build-type opt \
#	--tpls tpls-0.98.9 \
#        tpls-0.98.9 phongle-optimize_transport


