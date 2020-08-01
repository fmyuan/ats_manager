import sys
import argparse
import manager

def get_args():
    parser = argparse.ArgumentParser('Update ATS.')
    manager.get_update_args(parser, True)
    return parser.parse_args()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    args = get_args()

    rc, module = manager.update_ats(args.modulefile,
                                    recompile=(not args.skip_recompile),
                                    run_amanzi_tests=(not args.skip_amanzi_tests),
                                    run_ats_tests=(not args.skip_ats_tests))
    sys.exit(rc)
