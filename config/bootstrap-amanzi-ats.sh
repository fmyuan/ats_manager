./bootstrap.sh \
    --debug --relwithdebinfo_tpls --debug_trilinos \
    --enable-shared \
    --parallel=8 \
    --tools-mpi=openmpi --with-mpi=${MPI_DIR} \
    --amanzi-build-dir=${AMANZI_BUILD_DIR} --amanzi-install-prefix=${AMANZI_DIR} \
    --disable-structured \
    --disable-geochemistry \
    --disable-petsc \
    --disable-alquimia \
    --disable-pflotran \
    --disable-crunchtope \
    --enable-silo \
    --enable-ats_physics \
    --disable-amanzi_physics \
    --enable-clm \
    --ats_dev \
    --tpl-build-dir=${AMANZI_TPLS_BUILD_DIR} --tpl-install-prefix=${AMANZI_TPLS_DIR} \
    --tpl-download-dir=/Users/uec/codes/ats/amanzi-tpls/Downloads/ \
    --with-c-compiler=`which mpicc` --with-cxx-compiler=`which mpicxx` --with-fort-compiler=`which mpifort`


#    --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake
    




