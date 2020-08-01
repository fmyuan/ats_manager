import subprocess
import logging
import ats_manager.utils as utils

_make_test_cmd = \
"""#!/bin/env bash

echo "running make test"
module load {}
cd ${{AMANZI_BUILD_DIR}}
make test
"""

_regression_test_cmd = \
"""#!/bin/env bash

module load {}
echo "cd ${{ATS_TESTS_DIR}}"
cd ${{ATS_TESTS_DIR}}
python3 regression_tests.py -e `which ats` -m `which mpiexec` .
"""

def amanziUnitTests(modulefile):
    make_test_cmd = _make_test_cmd.format(modulefile)
    logging.debug(make_test_cmd)
    logging.info("Running Amanzi unit tests")
    logging.info(make_test_cmd)
    return utils.run_cmd('make_test', modulefile, make_test_cmd)

def atsRegressionTests(modulefile):
    regression_test_cmd = _regression_test_cmd.format(modulefile)
    logging.debug(regression_test_cmd)
    logging.info("Running ATS regression tests")
    return utils.run_cmd('ats_regression_test', modulefile, regression_test_cmd)
