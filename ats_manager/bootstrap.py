"""Sets up and runs bootstrap"""
import os,stat
import subprocess
import logging
import ats_manager.names as names
import ats_manager.utils as utils

def bootstrapExistingFromFile(module_name):
    logging.info('Bootstrap for: {}'.format(module_name))
    logging.info('Bootstrap: {}'.format(utils.script_name('bootstrap', module_name)))
    return utils.run_script('bootstrap', module_name)


def _set_arg(args, key, val):
    if val:
        args[key] = 'enable'
    else:
        args[key] = 'disable'
        

_compiler_tmp = "--with-c-compiler=`which {}` --with-cxx-compiler=`which {}` --with-fort-compiler=`which {}`"
def vendor_compilers(cc, cxx, fort):
    return _compiler_tmp.format(cc,cxx,fort)

def mpi_compilers():
    return _compiler_tmp.format('mpicc', 'mpicxx', 'mpifort')
    
        
_bootstrap_amanzi_template = \
"""#!/usr/bin/env bash
source ${{MODULESHOME}}/init/profile

{mpi}
module load {module_name}
cd ${{AMANZI_SRC_DIR}}


echo "Building Amanzi: {module_name}"
echo "-----------------------------------------------------"
echo "AMANZI_SRC_DIR = ${{AMANZI_SRC_DIR}}"
echo "AMANZI_BUILD_DIR= ${{AMANZI_BUILD_DIR}}"
echo "AMANZI_DIR = ${{AMANZI_DIR}}"
echo ""
echo "AMANZI_TPLS_BUILD_DIR = ${{AMANZI_TPLS_BUILD_DIR}}"
echo "AMANZI_TPLS_DIR = ${{AMANZI_TPLS_DIR}}"
echo "-----------------------------------------------------"

./bootstrap.sh \
    --${{AMANZI_BUILD_TYPE}} \
    --${{AMANZI_TRILINOS_BUILD_TYPE}}_trilinos \
    --${{AMANZI_TPLS_BUILD_TYPE}}_tpls \
    --parallel=8 \
    {shared_libs} \
    --tpl-build-dir=${{AMANZI_TPLS_BUILD_DIR}} \
    --tpl-install-prefix=${{AMANZI_TPLS_DIR}} \
    --amanzi-build-dir=${{AMANZI_BUILD_DIR}} \
    --amanzi-install-prefix=${{AMANZI_DIR}} \
    --tpl-download-dir=${{ATS_BASE}}/amanzi-tpls/Downloads {tpl_config_file} \
    --{structured}-structured \
    --{geochemistry}-geochemistry \
    --{geochemistry}-petsc \
    --{geochemistry}-alquimia \
    --{geochemistry}-pflotran \
    --{geochemistry}-crunchtope \
    --enable-amanzi_physics \
    --enable-hypre \
    --enable-silo \
    --enable-clm \
    --disable-ats_physics \
    {compilers} {flags} \
    --with-mpi=${{MPI_DIR}} \
    --with-python=`which python`

exit $?
""" 
def bootstrap_amanzi(module_name,
                     compilers=None,
                     mpi=None,
                     enable_structured=False,
                     enable_geochemistry=True,
                     use_existing_tpls=False,
                     bootstrap_options=None,
                     build_static=False):
    args = dict()
    args['module_name'] = module_name
    if mpi is not None:
        args['mpi'] = 'module load {}'.format(mpi)
    else:
        args['mpi'] = ''

    if build_static:
        args['shared_libs'] = '--disable-shared'
    else:
        args['shared_libs'] = '--enable-shared'

    _set_arg(args, 'structured', enable_structured)
    _set_arg(args, 'geochemistry', enable_geochemistry)

    if use_existing_tpls:
        args['tpl_config_file'] = "    --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake"
    else:
        args['tpl_config_file'] = ""


    args['compilers'] = mpi_compilers()
    if bootstrap_options is None:
        args['flags'] = ''
    else:
        args['flags'] = bootstrap_options

    logging.info('Filling  bootstrap')
    logging.info(args)
    cmd = _bootstrap_amanzi_template.format(**args)
    logging.info(cmd)
    
    return utils.run_cmd('bootstrap', module_name, cmd)
        

_bootstrap_ats_template = \
"""#!/usr/bin/env bash
source ${{MODULESHOME}}/init/profile

{mpi}
module load {module_name}
cd ${{AMANZI_SRC_DIR}}


echo "Building Amanzi-ATS: {module_name}"
echo "-----------------------------------------------------"
echo "AMANZI_SRC_DIR = ${{AMANZI_SRC_DIR}}"
echo "AMANZI_BUILD_DIR= ${{AMANZI_BUILD_DIR}}"
echo "AMANZI_DIR = ${{AMANZI_DIR}}"
echo ""
echo "AMANZI_TPLS_BUILD_DIR = ${{AMANZI_TPLS_BUILD_DIR}}"
echo "AMANZI_TPLS_DIR = ${{AMANZI_TPLS_DIR}}"
echo "-----------------------------------------------------"

./bootstrap.sh \
    --${{AMANZI_BUILD_TYPE}} \
    --${{AMANZI_TRILINOS_BUILD_TYPE}}_trilinos \
    --${{AMANZI_TPLS_BUILD_TYPE}}_tpls \
    --parallel=8 \
    {shared_libs} \
    --tpl-build-dir=${{AMANZI_TPLS_BUILD_DIR}} \
    --tpl-install-prefix=${{AMANZI_TPLS_DIR}} \
    --amanzi-build-dir=${{AMANZI_BUILD_DIR}} \
    --amanzi-install-prefix=${{AMANZI_DIR}} \
    --tpl-download-dir=${{ATS_BASE}}/amanzi-tpls/Downloads {tpl_config_file} \
    --disable-structured \
    --{geochemistry}-geochemistry \
    --{geochemistry}-petsc \
    --{geochemistry}-alquimia \
    --{geochemistry}-pflotran \
    --{geochemistry}-crunchtope \
    --disable-amanzi_physics \
    --enable-ats_physics \
    --enable-hypre \
    --enable-silo \
    --enable-clm \
    --enable-reg_tests \
    --ats_dev \
    {compilers} {flags} \
    --with-mpi=${{MPI_DIR}} \
    --with-python=`which python`

exit $?
""" 
def bootstrap_ats(module_name,
                  mpi=None,
                  enable_geochemistry=False,
                  use_existing_tpls=False,
                  bootstrap_options=None,
                  build_static=False):
    args = dict()
    args['module_name'] = module_name

    if mpi is not None:
        args['mpi'] = 'module load {}'.format(mpi)
    else:
        args['mpi'] = ''

    if build_static:
        args['shared_libs'] = '--disable-shared'
    else:
        args['shared_libs'] = '--enable-shared'
        
    _set_arg(args, 'geochemistry', enable_geochemistry)

    if use_existing_tpls:
        args['tpl_config_file'] = "    --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake"
    else:
        args['tpl_config_file'] = ""

    args['compilers'] = mpi_compilers()
    if bootstrap_options is None:
        args['flags'] = ''
    else:
        args['flags'] = bootstrap_options

        
    logging.info('Filling bootstrap command:')
    logging.info(args)
    cmd = _bootstrap_ats_template.format(**args)
    logging.info(cmd)

    return utils.run_cmd('bootstrap', module_name, cmd)
        



