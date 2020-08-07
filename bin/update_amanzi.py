import sys
import argparse
import ats_manager as manager

def get_args():
    parser = argparse.ArgumentParser('Update Amanzi.')
    manager.get_update_args(parser, False)
    return parser.parse_args()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    args = get_args()

    rc, module = manager.update_amanzi(args.modulefile,
                                        run_amanzi_tests=(not args.skip_amanzi_tests))
    sys.exit(rc)
