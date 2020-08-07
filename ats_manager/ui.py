import argparse

def get_install_args(parser, ats=False):
    parser.add_argument('amanzi_name', type=str,
                        help='Arbitrary but unique name of the Amanzi installation.  Typically the branch.')
    if ats:
        parser.add_argument('ats_name', type=str,
                            help='Arbitrary but unique name of the ATS installation.  Typically the branch.')
    
    parser.add_argument('--amanzi-branch', type=str, default=None,
                        help='(Existing) branch of Amanzi to install.')
    if ats:
        parser.add_argument('--ats-branch', type=str, default=None,
                            help='(Existing) branch of ATS to install.')
        
    parser.add_argument('--new-amanzi-branch', type=str, default=None,
                        help='Create a new branch of Amanzi.')
    if ats:
        parser.add_argument('--new-ats-branch', type=str, default=None,
                            help='Create a new branch of ATS.')
        
    parser.add_argument('--use-existing-tpls', default=None,
                        help='If supplied, use an existing TPL at this name.')
    parser.add_argument('--build-type', type=str, default='debug',
                        help='Amanzi build type, one of debug, opt, or relwithdebinfo')
    parser.add_argument('--tpls-build-type', type=str, default='relwithdebinfo',
                        help='TPLs build type, one of "debug", "opt", or "relwithdebinfo"')
    parser.add_argument('--trilinos-build-type', type=str, default='debug',
                        help='Trilinos build type, one of "debug", "opt", or "relwithdebinfo"')
    parser.add_argument('--tools-mpi', type=str, default=None,
                        help='Use a SuperBuild installed MPI of this type (openmpi, mpich)')
    parser.add_argument('--skip-amanzi-tests', action='store_true',
                        help='Skip running Amanzi tests.')
    if ats:
        parser.add_argument('--skip-ats-tests', action='store_true',
                            help='Skip running ATS tests.')
    parser.add_argument('--skip-clone', action='store_true',
                        help='Skip cloning (and use existing repos)')
    parser.add_argument('--clobber', action='store_true',
                        help='Clobber any existing repos.')
    
    parser.add_argument('--enable-geochemistry', action='store_true',
                        help='Build with geochemistry physics package')

    if not ats:
        parser.add_argument('--enable-structured', action='store_true',
                            help='Build with geochemistry physics package')
    return


def get_update_args(parser, ats=False):
    parser.add_argument('modulefile', type=str,
                        help='Name of the modulefile (e.g. ats/master/debug)')
    parser.add_argument('--skip-recompile', action='store_true',
                        help='Skip re-compiling.')
    parser.add_argument('--skip-amanzi-tests', action='store_true',
                        help='Skip running Amanzi tests.')
    if ats:
        parser.add_argument('--skip-ats-tests', action='store_true',
                            help='Skip running ATS tests.')
    return
