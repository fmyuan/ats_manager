./bootstrap.sh \
    --debug --relwithdebinfo_tpls --debug_trilinos \
    --enable-shared \
    --parallel=8 \
    --tools-mpi=openmpi --with-mpi=${MPI_DIR} \
    --tpl-build-dir=${AMANZI_TPLS_BUILD_DIR} --tpl-install-prefix=${AMANZI_TPLS_DIR} \
    --amanzi-build-dir=${AMANZI_BUILD_DIR} --amanzi-install-prefix=${AMANZI_DIR} \
    --tpl-download-dir=/Users/uec/codes/ats/amanzi-tpls/Downloads/ \
    --disable-structured \
    --disable-stk_mesh \
    --disable-petsc \
    --disable-alquimia \
    --disable-amanzi_physics \
    --disable-crunchtope \
    --disable-pflotran \
    --disable-geochemistry \
    --enable-ats_physics \
    --branch_ats=tpetra \
    --enable-kokkos


#    --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake    




