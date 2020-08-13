import sys
import argparse
import ats_manager as manager

def get_args():
    parser = argparse.ArgumentParser('Install ATS from a branch.')
    manager.get_install_args(parser, True)
    args = parser.parse_args()
    manager.set_default_args(args)
    return args
    
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    args = get_args()
    rc, module = manager.install_ats(**vars(args))
    sys.exit(rc)
    
