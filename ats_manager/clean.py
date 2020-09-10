"""Helper functions for cleaning builds."""

import os, shutil
import ats_manager.utils
import logging


def remove_dir(dirname, force=False):
    """Safely removes a directory"""
    if not os.path.exists(dirname):
        logging.info("Not removing nonexistent directory: {}".format(dirname))
        return 1
    
    ats_base = os.environ['ATS_BASE']
    if not len(ats_base) > 1:
        raise RuntimeError("Missing or invalid ATS_BASE")

    if not dirname.startswith(ats_base):
        # make sure dirname is in that directory
        logging.warning("Directory '{}' not in ATS_BASE='{}'".format(dirname, ats_base))
        return 1

    # make sure it has some extra info...
    if len(dirname) <= len(ats_base)+10:
        logging.warning("Directory '{}' seems like an awfully short name... cowardly refusing to remove.".format(dirname))
        return 1

    # make sure it doesn't escape back up the tree
    if '..' in dirname:
        logging.warning("Directory '{}' contains '..' which may go somewhere bad... cowardly refusing to remove.".format(dirname))
        return 1

    # confirm with user
    if not force:
        do_it = ats_manager.utils.query_yes_no('Really remove "{}"?'.format(dirname))
        if not do_it:
            return 1
    
    # what else can we check?
    logging.info('Removing: {}'.format(dirname))
    shutil.rmtree(dirname, True)
    return 0
    
        
