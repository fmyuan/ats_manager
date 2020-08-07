import sys
import argparse
import ats_manager as manager

def get_args():
    parser = argparse.ArgumentParser('Install ATS from a branch.')
    manager.get_install_args(parser, True)
    return parser.parse_args()
    
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    args = get_args()
    rc, module = manager.install_ats(args.amanzi_name, args.ats_name,args.use_existing_tpls,
                                     args.amanzi_branch, args.ats_branch,
                                     args.new_amanzi_branch, args.new_ats_branch,
                                     build_type=args.build_type,
                                     tpls_build_type=args.tpls_build_type,
                                     trilinos_build_type=args.trilinos_build_type,
                                     tools_mpi=args.tools_mpi,
                                     run_amanzi_tests=(not args.skip_amanzi_tests),
                                     run_ats_tests=(not args.skip_ats_tests),
                                     skip_clone=args.skip_clone,
                                     clobber=args.clobber,
                                     enable_geochemistry=args.enable_geochemistry)
    
    sys.exit(rc)
    
