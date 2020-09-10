import sys
import argparse
import ats_manager as manager

def get_args():
    parser = argparse.ArgumentParser(description="Clean build/install directories or completely remove a build.")
    manager.get_clean_args(parser)
    return parser.parse_args()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    args = get_args()
    rc, module = manager.clean(**vars(args))
    sys.exit(rc)
