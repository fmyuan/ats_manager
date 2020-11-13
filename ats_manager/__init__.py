import os, shutil
import git
import logging

import ats_manager.repo as repo
import ats_manager.names as names
import ats_manager.modulefile as modulefile
import ats_manager.bootstrap as bootstrap
import ats_manager.test_runner as test_runner
import ats_manager.clean as ats_clean

from ats_manager.ui import *

def install_ats(amanzi_name, ats_name,
                amanzi_branch=None, ats_branch=None,
                new_amanzi_branch=None, new_ats_branch=None,
                build_type='debug',
                tpls_build_type='relwithdebinfo',
                trilinos_build_type='debug',
                mpi=None,
                tpls=None,
                skip_amanzi_tests=False,
                skip_ats_tests=False,
                skip_clone=False,
                clobber=False,
                **kwargs):
    """Create a new ATS installation.

    Creates a modulefile, clones the repos, bootstraps the code, and
    runs the tests.

    To see arguments, run: `python bin/install_ats.py -h`

    Returns
    -------
    int : return code: 
        0 = success
       -1 = failed build
       >0 = successful build but failing tests
    str : name of the generated modulefile

    """
    logging.info('Installing ATS:')
    logging.info('=============================================================================')
    logging.info('ATS name: {}'.format(ats_name))
    logging.info('Amanzi name: {}'.format(amanzi_name))
    logging.info('ATS branch: {}'.format(ats_branch))
    logging.info('Amanzi branch: {}'.format(amanzi_branch))
    logging.info('ATS new branch: {}'.format(new_ats_branch))
    logging.info('Amanzi new branch: {}'.format(new_amanzi_branch))

    name = names.filename(amanzi_name, ats_name, build_type, mpi)
    repo_name = names.filename(new_amanzi_branch, new_ats_branch, build_type, mpi)

    if tpls is None:
        name_split = name.split('/')
        tpls_name = names.filename(amanzi_name, None, tpls_build_type, mpi, prefix='amanzi-tpls')
        use_existing_tpls = False
    else:
        tpls_name = names.filename(tpls, None, tpls_build_type, mpi, prefix='amanzi-tpls')
        use_existing_tpls = True

    if use_existing_tpls:
        logging.info('Using existing TPLs: {}'.format(tpls_name))
    else:
        logging.info('Building TPLs: {}'.format(tpls_name))
    logging.info('with MPI: {}'.format(mpi))        
    logging.info('---------------')
    logging.info('Fully resolved name: {}'.format(name))
    logging.info('Fully resolved repo: {}'.format(repo_name))
    logging.info('Fully resolved TPLs: {}'.format(tpls_name))
    logging.info('=============================================================================')

    logging.info('Generating module file:')
    template_params = modulefile.create_modulefile(name, repo_name, tpls_name,
                                 build_type=build_type,
                                 tpls_build_type=tpls_build_type,
                                 trilinos_build_type=trilinos_build_type,
                                 mpi=mpi)
                                 
    logging.info('=============================================================================')
    # clone the repo
    logging.info('Setting up repo:  clone = {}, clobber = {}'.format(skip_clone, clobber))
    if skip_clone:
        amanzi_repo = git.Repo(template_params['amanzi_src_dir'])
    else:
        if clobber:
            ats_clean.remove_dir(template_params['amanzi_src_dir'], True)
        amanzi_repo = repo.clone_amanzi_ats(template_params['amanzi_src_dir'], amanzi_branch, ats_branch)
    
    if new_amanzi_branch != amanzi_branch:
        amanzi_repo.git.checkout('-b', new_amanzi_branch)
    if new_ats_branch != ats_branch:
        amanzi_repo.submodule(names.ats_submodule).module().git.checkout('-b', new_ats_branch)

    logging.info('=============================================================================')
    logging.info('Calling bootstrap:')
    # bootstrap, make, install
    rc = bootstrap.bootstrap_ats(name, use_existing_tpls=use_existing_tpls, mpi=mpi, **kwargs)
    if rc != 0:
        return -1, name

    # amanzi make tests
    if skip_amanzi_tests:
        amanzi_unittests_rc = 0
    else:
        amanzi_unittests_rc = test_runner.amanziUnitTests(name)
        if amanzi_unittests_rc != 0:
            rc += 1
    return rc, name


def install_amanzi(amanzi_name,
                   amanzi_branch=None,
                   new_amanzi_branch=None,
                   build_type='debug',
                   tpls_build_type='relwithdebinfo',
                   trilinos_build_type='debug',
                   mpi=None,
                   tpls=None,
                   skip_amanzi_tests=False,
                   skip_clone=False,
                   clobber=False,
                   **kwargs):
    """Create a new Amanzi installation.

    Creates a modulefile, clones the repos, bootstraps the code, and
    runs the tests.

    To see arguments, run: `python bin/install_amanzi.py -h`

    Returns
    -------
    int : return code: 
        0 = success
       -1 = failed build
       >0 = successful build but failing tests
    str : name of the generated modulefile

    """
    logging.info('Installing Amanzi:')
    logging.info('=============================================================================')
    logging.info('Amanzi name: {}'.format(amanzi_name))
    logging.info('Amanzi branch: {}'.format(amanzi_branch))
    logging.info('Amanzi new branch: {}'.format(new_amanzi_branch))

    name = names.filename(amanzi_name, None, build_type, mpi)
    repo_name = names.filename(new_amanzi_branch, None, build_type, mpi)

    if tpls is None:
        name_split = name.split('/')
        tpls_name = names.filename(amanzi_name, None, tpls_build_type, mpi, prefix='amanzi-tpls')
        use_existing_tpls = False
    else:
        tpls_name = names.filename(tpls, None, tpls_build_type, mpi, prefix='amanzi-tpls')
        use_existing_tpls = True

    if use_existing_tpls:
        logging.info('Using existing TPLs: {}'.format(tpls_name))
    else:
        logging.info('Building TPLs: {}'.format(tpls_name))
    logging.info('with MPI: {}'.format(mpi))        
    logging.info('---------------')
    logging.info('Fully resolved name: {}'.format(name))
    logging.info('Fully resolved repo: {}'.format(repo_name))
    logging.info('Fully resolved TPLs: {}'.format(tpls_name))
    logging.info('=============================================================================')

    logging.info('Generating module file:')
    template_params = modulefile.create_modulefile(name, repo_name, tpls_name,
                                                   build_type=build_type,
                                                   tpls_build_type=tpls_build_type,
                                                   trilinos_build_type=trilinos_build_type,
                                                   mpi=mpi)
                                 
    logging.info('=============================================================================')
    # clone the repo
    logging.info('Setting up repo:  clone = {}, clobber = {}'.format(skip_clone, clobber))
    if skip_clone:
        amanzi_repo = git.Repo(template_params['amanzi_src_dir'])
    else:
        if clobber:
            ats_clean.remove_dir(template_params['amanzi_src_dir'], True)
        amanzi_repo = repo.clone_amanzi(template_params['amanzi_src_dir'], amanzi_branch)
         
    if new_amanzi_branch != amanzi_branch:
        amanzi_repo.git.checkout('-b', new_amanzi_branch)

    logging.info('=============================================================================')
    logging.info('Calling bootstrap:')
    # bootstrap, make, install
    rc = bootstrap.bootstrap_amanzi(name, use_existing_tpls=use_existing_tpls,
                                    mpi=mpi, **kwargs)
    if rc != 0:
        return -1, name

    # amanzi make tests
    if skip_amanzi_tests:
        amanzi_unittests_rc = 0
    else:
        amanzi_unittests_rc = test_runner.amanziUnitTests(name)
        if amanzi_unittests_rc != 0:
            rc += 1

    return rc, name



def update_ats(module_name,
               recompile=True,
               run_amanzi_tests=True,
               run_ats_tests=True):
    assert(module_name.startswith('ats'))
    amanzi_name, ats_name, build_type, compilers = names.split_filename(module_name)

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
            return rc, module_name

    # make test
    if run_amanzi_tests:
        amanzi_unittests_rc = test_runner.amanziUnitTests(module_name)
        if amanzi_unittests_rc != 0:
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


def update_amanzi(module_name,
                  recompile=True,
                  run_amanzi_tests=True):
    assert(module_name.startswith('amanzi'))
    amanzi_name, _, build_type, compilers = names.split_filename(module_name)

    # pull Amanzi
    src_dir = names.amanzi_src_dir(module_name)
    logging.info('Pulling Amanzi at: {}'.format(src_dir))
    amanzi_repo = git.Repo(src_dir)
    amanzi_repo.git.pull()

    rc = 0
    # recompile
    if recompile:
        rc = bootstrap.bootstrapExistingFromFile(module_name)
        if (rc != 0):
            return rc, module_name

    # make test
    if run_amanzi_tests:
        amanzi_unittests_rc = test_runner.amanziUnitTests(module_name)
        if amanzi_unittests_rc != 0:
            rc += 1

    return rc, module_name

def clean(module_name, remove=False, force=False):
    """Cleans or completely removes a build.

    By defualt, this removes: 
     * AMANZI_BUILD_DIR
     * AMANZI_DIR
     * AMANZI_TPLS_BUILD_DIR
     * AMANZI_TPLS_DIR

    If remove == True, this also removes:
     * AMANZI_SRC_DIR
     * modulefile
     * all bootstrap scripts
     * any test directories

    """
    amanzi_install_dir = names.amanzi_install_dir(module_name)
    ats_clean.remove_dir(amanzi_install_dir, force)

    amanzi_build_dir = names.amanzi_build_dir(module_name)
    ats_clean.remove_dir(amanzi_build_dir, force)

    tpls_install_dir = names.tpls_install_dir(module_name)
    ats_clean.remove_dir(tpls_install_dir, force)

    tpls_build_dir = names.tpls_build_dir(module_name)
    ats_clean.remove_dir(tpls_build_dir, force)

    if remove:
        amanzi_src_dir = names.amanzi_src_dir(module_name)
        ats_clean.remove_dir(amanzi_src_dir, force)

        bootstrap_script = utils.script_name('bootstrap', module_name)
        if os.path.exists(bootstrap_script):
            os.remove(bootstrap_script)

        modulefile = names.modulefile_path(module_name)
        if os.path.exists(modulefile):
            os.remove(modulefile)

    return 0, module_name
    
    
          
