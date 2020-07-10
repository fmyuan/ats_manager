./bootstrap.sh \
    --debug --relwithdebinfo_tpls --debug_trilinos \
    --enable-shared \
    --parallel=8 \
    --tpl-build-dir=${AMANZI_TPLS_BUILD_DIR} --tpl-install-prefix=${AMANZI_TPLS_DIR} \
    --amanzi-build-dir=${AMANZI_BUILD_DIR} --amanzi-install-prefix=${AMANZI_DIR} \
    --tools-mpi=openmpi \
    --tools-build-dir=/Users/uec/codes/ats/tools/build \
    --tools-install-prefix=/Users/uec/codes/ats/tools/install \
    --tools-download-dir=/Users/uec/codes/ats/tools/Downloads \
    --tpl-download-dir=/Users/uec/codes/ats/amanzi-tpls/Downloads/ \
    --enable-structured \
    --enable-geochemistry \
    --enable-amanzi_physics \
    --enable-silo \
    --enable-hypre \
    --enable-clm \
    --disable-ats_physics
    

