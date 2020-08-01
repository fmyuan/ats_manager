import os,shutil
import logging
import git

import ats_manager.names as names

def clone(name, url, path, branch='master', clobber=False):
    """Generic clone helper"""
    if os.path.exists(path):
        if clobber:
            shutil.rmtree(path)
        else:
            raise RuntimeError("Cannot clone into {} as it already exists.")

    logging.info('Cloning {}'.format(name))
    logging.info('   from: {}'.format(url))
    logging.info('     to: {}'.format(path))
    logging.info(' branch: {}'.format(branch))
    return git.Repo.clone_from(url, path, branch=branch)

def clone_amanzi(path, branch='master', clobber=False):
    """Clones a new copy of an Amanzi branch."""
    return clone('Amanzi', names.amanzi_url, path, branch, clobber)

def clone_amanzi_ats(path, branch='master', ats_branch=None, clobber=False):
    """Clones a new copy of an Amanzi branch that includes ATS."""
    repo = clone_amanzi(path, branch, clobber=clobber)

    ats_sub = repo.submodule(names.ats_submodule)
    logging.info('Cloning submodules (ATS).')
    ats_sub.update(init=True)
    if ats_branch is not None:
        logging.info('Checking out ATS branch: {}'.format(ats_branch))
        ats_sub.module().git.checkout(ats_branch)
        ats_sub.module().git.pull()
    return repo

def clone_ats_regression_tests(path, branch='master', clobber=False):
    return clone('ATS regression tests', names.ats_regression_tests_url, path, branch, clobber)

def new_branch(repo, branch):
    repo.git.checkout('-b', branch)
    



        
