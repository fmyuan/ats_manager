import subprocess
import logging
import ats_manager.utils as utils

_make_test_cmd = \
"""#!/usr/bin/env bash
source ${{MODULESHOME}}/init/profile

echo "running make test"
module load {}
cd ${{AMANZI_BUILD_DIR}}
make test
"""

def amanziUnitTests(modulefile):
    make_test_cmd = _make_test_cmd.format(modulefile)
    logging.debug(make_test_cmd)
    logging.info("Running Amanzi unit tests")
    logging.info(make_test_cmd)
    return utils.run_cmd('make_test', modulefile, make_test_cmd)
