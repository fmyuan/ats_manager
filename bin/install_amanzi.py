import sys
import argparse
import ats_manager as manager

def get_args():
    parser = argparse.ArgumentParser('Install Amanzi from a branch.')
    manager.get_install_args(parser, False)
    return parser.parse_args()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    args = get_args()
    rc, module = manager.install_amanzi(args.amanzi_name, args.use_existing_tpls,
                                        args.amanzi_branch,
                                        args.new_amanzi_branch,
                                        build_type=args.build_type,
                                        tpls_build_type=args.tpls_build_type,
                                        trilinos_build_type=args.trilinos_build_type,
                                        mpi=args.mpi,
                                        run_amanzi_tests=(not args.skip_amanzi_tests),
                                        skip_clone=args.skip_clone,
                                        clobber=args.clobber,
                                        enable_structured=args.enable_structured,
                                        enable_geochemistry=args.enable_geochemistry)
    
    sys.exit(rc)
    
