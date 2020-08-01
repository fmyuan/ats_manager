import os, shutil
import git
import logging

import ats_manager.repo as repo
import ats_manager.names as names
import ats_manager.modulefile as modulefile
import ats_manager.bootstrap as bootstrap
import ats_manager.test_runner as test_runner

from ats_manager.ui import *

def install_ats(amanzi_name, ats_name, tpls_name=None,
                amanzi_branch=None, ats_branch=None,
                new_amanzi_branch=None, new_ats_branch=None,
                build_type='debug',
                tpls_build_type='relwithdebinfo',
                trilinos_build_type='debug',
                tools_mpi=False,
                run_amanzi_tests=True,
                run_ats_tests=True,
                skip_clone=False,
                **kwargs):
    """Create a new ATS installation.

    Creates a modulefile, clones the repos, bootstraps the code, and
    runs the tests.
    
    Parameters
    ----------
    amanzi_name, ats_name : str
      Arbitrary names to uniquely identify paths for Amanzi and ATS to
      be installed.  Note these must be unique relative to previously
      created installations.
    tpls_name : str, optional
      If provided, use an existing tpl installation from an Amanzi
      previously installed where this value was given as 'amanzi_name'
    amanzi_branch, ats_branch : str, optional
      Amanzi and ATS branches to clone.  If None, set to the same as
      amanzi_name and ats_name, respectively (default behavior).  If
      ats_branch is 'default', uses the submodule info from the Amanzi
      branch.
    new_amanzi_branch, new_ats_branch : str, optional
      Create a new Amanzi or ATS branch if provided, starting from
      amanzi_branch and ats_branch, respectively.
    build_type, tpls_build_type, trilinos_build_type : str, optional
      One of 'debug', 'opt', or 'relwithdebinfo'.  The build type of
      the run.  Default to 'debug', 'relwithdebinfo', and 'debug'
      respectively.
    tools_mpi : bool, optional
      If True, use the MPI installed by SuperBuild.  If False
      (default), use the MPI at os.environ['MPI_DIR'].
    run_amanzi_tests, run_ats_tests : bool, optional
      If True (default), run Amanzi unittests and ATS regression
      tests, respectively.
    skip_clone : bool, optional
      If True, use the existing repo.

    Additional Parameters
    ---------------------
    All additional parameters are passed to
    ats_manager.bootstrap.bootstrap_ats().  Most commonly, these include:

    enable_geochemistry : bool, optional
      If True, build Amanzi and ATS with chemistry and TPLs with
      Alquimia, PFloTran, PETSc, and CrunchTope.  Default is False.
    enable_kokkos_* : bool, optional
      If True, build a Kokkos + Tpetra "Amanzi-ATS 2.0" suite of TPLs,
      Amanzi, and ATS, and turn on specific Kokkos backends.  Default
      is False.  Most common are enable_kokkos_cuda and
      enable_kokkos_openmp.
    arch : str, optional
      Specify bootstrap-recognized arch flag.  Currently only Summit
      and NERSC are supported.  Default is None.

    Returns
    -------
    int : return code: 
        0 = success
       -1 = failed build
       >0 = successful build but failing tests
    str : name of the generated modulefile

    """
    assert(build_type in names.valid_build_types)
    assert(trilinos_build_type in names.valid_build_types)
    assert(tpls_build_type in names.valid_build_types)

    if amanzi_branch is None:
        amanzi_branch = amanzi_name
    if new_amanzi_branch is None:
        new_amanzi_branch = amanzi_branch
    
    if ats_name is None:
        ats_name = "default"
        assert(ats_branch is None)
        assert(new_ats_branch is None)
    else:
        if ats_branch is None:
            ats_branch = ats_name
        if new_ats_branch is None:
            new_ats_branch = ats_branch

    name = names.filename(amanzi_name, ats_name, build_type)
    repo_name = names.filename(new_amanzi_branch, new_ats_branch, build_type)

    if tpls_name is None:
        name_split = name.split('/')
        tpls_name = '/'.join('amanzi-tpls',name_split[1],tpls_build_type)
        use_existing_tpls = False
    else:
        tpls_name = names.filename(tpls_name, None, tpls_build_type, prefix='amanzi-tpls')
        use_existing_tpls = True

    logging.info('Installing ATS:')
    logging.info('=============================================================================')
    logging.info('ATS name: {}'.format(ats_name))
    logging.info('Amanzi name: {}'.format(amanzi_name))
    if use_existing_tpls:
        logging.info('Using existing TPLs: {}'.format(tpls_name))
    else:
        logging.info('Building TPLs: {}'.format(tpls_name))
        
    logging.info('---------------')
    logging.info('ATS branch: {}'.format(ats_branch))
    logging.info('Amanzi branch: {}'.format(amanzi_branch))
    if new_ats_branch != ats_branch:
        logging.info('ATS new branch: {}'.format(new_ats_branch))
    if new_amanzi_branch != amanzi_branch:
        logging.info('Amanzi new branch: {}'.format(new_amanzi_branch))
    logging.info('---------------')
    logging.info('Fully resolved name: {}'.format(name))
    logging.info('Fully resolved repo: {}'.format(repo_name))
    logging.info('Fully resolved TPLs: {}'.format(tpls_name))
    logging.info('=============================================================================')

    if tools_mpi:
        mpi_dir = names.tools_mpi_dir()
    else:
        mpi_dir = os.environ['MPI_DIR']
        
    logging.info('Generating module file:')
    template_params = modulefile.create_modulefile(name, repo_name, tpls_name,
                                 build_type=build_type,
                                 tpls_build_type=tpls_build_type,
                                 trilinos_build_type=trilinos_build_type,
                                 mpi_dir=mpi_dir)
                                 
    logging.info('=============================================================================')
    # clone the repo
    if skip_clone:
        amanzi_repo = git.Repo(template_params['amanzi_src_dir'])
    else:
        # -- double check before clobbering dangerously
        ats_base = os.environ['ATS_BASE']
        assert(len(ats_base) > 1)
        assert(template_params['amanzi_src_dir'].startswith(ats_base))
        assert(len(template_params['amanzi_src_dir']) > len(ats_base)+10)
        if os.path.isdir(template_params['amanzi_src_dir']):
            shutil.rmtree(template_params['amanzi_src_dir'])
        amanzi_repo = repo.clone_amanzi_ats(template_params['amanzi_src_dir'], amanzi_branch, ats_branch)
    
    if new_amanzi_branch != amanzi_branch:
        amanzi_repo.git.checkout('-b', new_amanzi_branch)
    if new_ats_branch != ats_branch:
        amanzi_repo.submodule(names.ats_submodule).module().git.checkout('-b', new_ats_branch)

    # clone regression tests
    try:
        reg_test_repo = repo.clone_ats_regression_tests(template_params['ats_regression_tests_dir'],
                                                        ats_branch)
    except git.GitCommandError:
        # likely failed because branch doesn't exist -- clone master
        # and check a new branch out
        reg_test_repo = repo.clone_ats_regression_tests(template_params['ats_regression_tests_dir'])
        current_reg_branch = 'master'
    else:
        current_reg_branch = ats_branch
        
    if new_ats_branch != current_reg_branch:
        reg_test_repo.git.checkout('-b', new_ats_branch)
        
    # bootstrap, make, install
    rc = bootstrap.bootstrap_ats(name, use_existing_tpls=use_existing_tpls, **kwargs)
    if rc is not 0:
        return -1

    # amanzi make tests
    if run_amanzi_tests:
        amanzi_unittests_rc = test_runner.amanziUnitTests(name)
        if amanzi_unittests_rc is not 0:
            rc += 1
    else:
        amanzi_unittests_rc = 0

    # ats regression tests
    if run_ats_tests:
        ats_regtests_rc = test_runner.atsRegressionTests(name)
        if ats_regtests_rc is not 0:
            rc += 1
    else:
        ats_regtests_rc = 0

    return rc, name


def install_amanzi(amanzi_name, tpls_name=None,
                   amanzi_branch=None,
                   new_amanzi_branch=None,
                   build_type='debug',
                   tpls_build_type='relwithdebinfo',
                   trilinos_build_type='debug',
                   tools_mpi=False,
                   run_amanzi_tests=True,
                   skip_clone=False,
                   **kwargs):
    """Create a new Amanzi installation.

    Creates a modulefile, clones the repos, bootstraps the code, and
    runs the tests.
    
    Parameters
    ----------
    amanzi_name : str
      Arbitrary name to uniquely identify paths for Amanzi.  Note
      these must be unique relative to previously created
      installations.
    tpls_name : str, optional
      If provided, use an existing tpl installation from an Amanzi
      previously installed where this value was given as 'amanzi_name'
    amanzi_branch : str, optional
      Amanzi branch to clone.  If None, set to the same as amanzi_name
      (default behavior).
    new_amanzi_branch : str, optional
      Create a new Amanzi branch if provided, starting from
      amanzi_branch.
    build_type, tpls_build_type, trilinos_build_type : str, optional
      One of 'debug', 'opt', or 'relwithdebinfo'.  The build type of
      the run.  Default to 'debug', 'relwithdebinfo', and 'debug'
      respectively.
    tools_mpi : bool, optional
      If True, use the MPI installed by SuperBuild.  If False
      (default), use the MPI at os.environ['MPI_DIR'].
    run_amanzi_tests : bool, optional
      If True (default), run Amanzi unittests.
    skip_clone : bool, optional
      If True, use the existing repo.

    Additional Parameters
    ---------------------
    All additional parameters are passed to
    ats_manager.bootstrap.bootstrap_ats().  Most commonly, these include:

    enable_structured : bool, optional
      If True, build Amanzi's structured capability too.
    enable_geochemistry : bool, optional
      If True, build Amanzi and ATS with chemistry and TPLs with
      Alquimia, PFloTran, PETSc, and CrunchTope.  Default is False.
    enable_kokkos_* : bool, optional
      If True, build a Kokkos + Tpetra "Amanzi-ATS 2.0" suite of TPLs,
      Amanzi, and ATS, and turn on specific Kokkos backends.  Default
      is False.  Most common are enable_kokkos_cuda and
      enable_kokkos_openmp.
    arch : str, optional
      Specify bootstrap-recognized arch flag.  Currently only Summit
      and NERSC are supported.  Default is None.

    Returns
    -------
    int : return code: 
        0 = success
       -1 = failed build
       >0 = successful build but failing tests
    str : name of the generated modulefile

    """
    assert(build_type in names.valid_build_types)
    assert(trilinos_build_type in names.valid_build_types)
    assert(tpls_build_type in names.valid_build_types)
    
    if amanzi_branch is None:
        amanzi_branch = amanzi_name
    if new_amanzi_branch is None:
        new_amanzi_branch = amanzi_branch

    name = names.filename(amanzi_name, None, build_type)
    repo_name = names.filename(new_amanzi_branch, None, build_type)

    if tpls_name is None:
        name_split = name.split('/')
        tpls_name = '/'.join('amanzi-tpls',name_split[1],tpls_build_type)
        use_existing_tpls = False
    else:
        tpls_name = names.filename(tpls_name, None, tpls_build_type, prefix='amanzi-tpls')
        use_existing_tpls = True

    logging.info('Installing Amanzi:')
    logging.info('------------------')
    logging.info('Amanzi name: {}'.format(amanzi_name))
    logging.info('Amanzi branch: {}'.format(amanzi_branch))
    logging.info('Amanzi new branch: {}'.format(new_amanzi_branch))
    logging.info('------------------')
    logging.info('Fully resolved name: {}'.format(name))
    logging.info('Fully resolved repo: {}'.format(repo_name))
    logging.info('Fully resolved TPLs: {}'.format(tpls_name))
    logging.info('------------------')

        
    if tools_mpi:
        mpi_dir = names.tools_mpi_dir()
    else:
        mpi_dir = os.environ['MPI_DIR']
        
    logging.info('Generating module file:')
    template_params = modulefile.create_modulefile(name, repo_name, tpls_name,
                                 build_type=build_type,
                                 tpls_build_type=tpls_build_type,
                                 trilinos_build_type=trilinos_build_type,
                                 mpi_dir=mpi_dir)
                                 
    # clone the repo
    if skip_clone:
        amanzi_repo = git.Repo(template_params['amanzi_src_dir'])
    else:
        # -- double check before clobbering dangerously
        ats_base = os.environ['ATS_BASE']
        assert(len(ats_base) > 1)
        assert(template_params['amanzi_src_dir'].startswith(ats_base))
        assert(len(template_params['amanzi_src_dir']) > len(ats_base)+10)
        shutil.rmtree(template_params['amanzi_src_dir'])
        amanzi_repo = repo.clone_amanzi_ats(template_params['amanzi_src_dir'], amanzi_branch)
    
    if new_amanzi_branch != amanzi_branch:
        amanzi_repo.git.checkout('-b', new_amanzi_branch)
        
    # bootstrap, make, install
    rc = bootstrap.bootstrap_amanzi(name, use_existing_tpls=use_existing_tpls, **kwargs)
    if rc is not 0:
        return -1

    # amanzi make tests
    if run_amanzi_tests:
        amanzi_unittests_rc = test_runner.amanziUnitTests(name)
        if amanzi_unittests_rc is not 0:
            rc += 1
    else:
        amanzi_unittests_rc = 0

    return rc, name



def update_ats(module_name,
               recompile=True,
               run_amanzi_tests=True,
               run_ats_tests=True):
    assert(module_name.startswith('ats'))
    amanzi_name, ats_name, build_type = names.split_filename(module_name)

    # pull Amanzi
    src_dir = names.amanzi_src_dir(module_name)
    logging.info('Pulling Amanzi at: {}'.format(src_dir))
    amanzi_repo = git.Repo(src_dir)
    amanzi_repo.git.pull()

    # pull ATS
    if ats_name == 'default':
        logging.info('Updating ATS to submodule head')
        amanzi_repo.git.submodule('update')
    else:
        ats_submodule = amanzi_repo.submodule(names.ats_submodule)
        ats_repo = ats_submodule.module()
        logging.info('Pulling ATS from branch: {}'.format(ats_repo.active_branch))
        ats_repo.git.pull()

    rc = 0
    # recompile
    if recompile:
        rc = bootstrap.bootstrapExistingFromFile(module_name)
        if (rc != 0):
            return rc

    # make test
    if run_amanzi_tests:
        amanzi_unittests_rc = test_runner.amanziUnitTests(module_name)
        if amanzi_unittests_rc is not 0:
            rc += 1

    # regression tests
    if run_ats_tests:
        ats_regtests_rc = test_runner.atsRegressionTests(module_name)
        if ats_regtests_rc is not 0:
            rc += 1

    if rc == 0 and ats_name != 'default':
        if ats_submodule.binsha != ats_repo.head.commit.binsha:
            # ats submodule has changed
            commit_msg = "Updated ATS to current HEAD of {}".format(ats_repo.active_branch)
            logging.info(commit_msg)

            ats_submodule.binsha = ats_repo.head.commit.binsha
            amanzi_repo.index.add([ats_submodule])
            amanzi_repo.index.commit(commit_msg)
            logging.info("Pushing to Amanzi origin")
            amanzi_repo.remote(name='origin').push()

    return rc, module_name

def installAmanziFromBranch(amanzi_name, tpls_name,
                            amanzi_branch='master',
                            use_existing_tpls=False,
                            build_type='debug',
                            tpls_build_type='relwithdebinfo',
                            trilinos_build_type='debug',
                            tools_mpi=False,
                            run_amanzi_tests=True,
                            **kwargs):
    """Create a new Amanzi installation from existing branches.

    Creates a modulefile, clones the repos, bootstraps the code, and
    runs the tests.
    
    Parameters
    ----------
    amanzi_name, tpls_name : str
      Arbitrary names to uniquely identify paths for Amanzi and
      TPLs to be installed.  Note these must be unique relative to
      previously created installations.
    amanzi_branch : str, optional
      Amanzi branches to clone.  Default is 'master'.
    use_existing_tpls : bool, optional
      If True, use the existing TPLs installation at tpls_name.  If
      False, install a new set of TPLs at tpls_name.  Default is
      False.
    build_type, tpls_build_type, trilinos_build_type : str, optional
      One of 'debug', 'opt', or 'relwithdebinfo'.  The build type of
      the run.  Default to 'debug', 'relwithdebinfo', and 'debug'
      respectively.
    tools_mpi : bool, optional
      If True, use the MPI installed by SuperBuild.  If False
      (default), use the MPI at os.environ['MPI_DIR'].
    run_amanzi_tests : bool, optional
      If True (default), run Amanzi unittests after installation.

    Additional Parameters
    ---------------------
    All additional parameters are passed to
    ats_manager.bootstrap.bootstrap_amanzi().  Most commonly, these include:

    enable_structured : bool, optional
      If True, build Amanzi's structured capabilities.  Default is
      False.
    enable_geochemistry : bool, optional
      If True, build Amanzi with chemistry and TPLs with
      Alquimia, PFloTran, PETSc, and CrunchTope.  Default is True.
    enable_kokkos_* : bool, optional
      If True, build a Kokkos + Tpetra "Amanzi-ATS 2.0" suite of TPLs
      and Amanzi, and turn on specific Kokkos backends.  Default
      is False.  Most common are enable_kokkos_cuda and
      enable_kokkos_openmp.
    arch : str, optional
      Specify bootstrap-recognized arch flag.  Currently only Summit
      and NERSC are supported.  Default is None.

    Returns
    -------
    int : return code: 
        0 = success
       -1 = failed build
       >0 = successful build but failing tests
    str : name of the generated modulefile

    """
    # generate the Amanzi modulefile
    module_name = mm.module_filename(amanzi_name, None, build_type)
    module_abs_path = mm.outputFilename(amanzi_name, None, build_type)
    temp_file = mm.templateName(True)
    temp_args = mm.amanzi_modulefile_template_args(amanzi_name, tpls_name, amanzi_branch,
                                                build_type, tpls_build_type, trilinos_build_type,
                                                tools_mpi)
    mm.fill_template(temp_file, module_abs_path, temp_args)

    # clone the repo
    amanzi_repo = mr.amanziFromBranch(amanzi_name, build_type, amanzi_branch)

    # bootstrap, make, install
    rc = mb.bootstrapAmanzi(mfile, **kwargs)
    if rc is not 0:
        return -1

    # amanzi make tests
    if run_amanzi_tests:
        amanzi_unittests_rc = mtr.amanziUnitTests(module_name)
        if amanzi_unittests_rc is not 0:
            rc += 1
    else:
        amanzi_unittests_rc = 0

    return rc, module_name
        


def updateAndTestAmanzi(module_name,
                        run_amanzi_tests=True):
    mfile_split = os.path.split(module_name)
    assert(mfile_split[0] == 'amanzi')
    amanzi_name = mfile_split[1]
    build_type = mfile_split[2]

    # pull Amanzi
    src_dir = mm.amanziSrcDir(amanzi_name, ats_name)
    logging.info('Pulling Amanzi at: {}'.format(src_dir))
    amanzi_repo = git.Repo(src_dir)
    amanzi_repo.git.pull()

    # recompile
    rc = mb.bootstrapExistingFromFile(module_name, amanzi_name, None, build_type)
    if (rc != 0):
        return rc

    # make test
    amanzi_unittests_rc = mtr.amanziUnitTests(module_name)
    if amanzi_unittests_rc is not 0:
        rc += 1

    return rc
