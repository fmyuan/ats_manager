import argparse

def fill(file_in, file_out, **kwargs):
    with open(file_in,'r') as fin:
        lines = file_in.readlines()

    lines.replace(**kwargs)
    with open(file_out, 'w') as fout:
        fout.write(lines)
    return

def get_arg_parser():
    parser = argparse.ArgumentParser('Writes a modulefile from template')
    parser.add_argument('--ats', type=str,
                        help='ATS directory')
    parser.add_argument('--ats-repo', type=str,
                        help='ATS repo (default is same as directory)')
    parser.add_argument('--amanzi', type=str,
                        help='Amanzi directory',
                        default='master')
    parser.add_argument('--amanzi-repo', type=str,
                        help='Amanzi repo (default is same as directory)',
                        default='master')
    parser.add_argument('--tpls', type=str,
                        help='TPLs directory',
                        default='master')
    parser.add_argument('--build-type', type=str,
                        help='Type of build',
                        default='Debug')
    parser.add_argument('--trilinos-build-type', type=str,
                        help='Type of build',
                        default=None)
    parser.add_argument('--tpls-build-type', type=str,
                        help='Type of build',
                        default='RelWithDebInfo')
    parser.add_argument('--tools-mpi', type=bool,
                        action='store_true',
                        help='Use bootstrap MPI')
    parser.add_argument('file', type=str,
                        help='Module file name, e.g. ats/master/Debug')
    return parser



if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()

    # set the template file
    if args.ats == 'none':
        template = os.path.join(os.environ['ATS_BASE'], 'bin', 'templates',
                                'amanzi_modulefile.template')
    else:
        template = os.path.join(os.environ['ATS_BASE'], 'bin', 'templates',
                                'ats_modulefile.template')

    # set the output file
    outfile_root = os.environ['ATS_BASE']
    outfile = os.path.join(outfile_root, modulefiles, args.file)
    outfile_dir = os.path.join(os.path.split(outfile)[:-1])
    os.mkdir(outfile_dir)

    # trilinos build_type arg
    if args.trilinos_build_type is None:
        args.trilinos_build_type = args.build_type

    # repo arguments
    if args.amanzi_repo is None:
        args.amanzi_repo = args.amanzi
    if args.ats_repo is None:
        args.ats_repo = args.ats
        
    # set mpi_dir
    if args.tools_mpi:
        args.mpi_dir = os.path.join(os.environ['ATS_BASE'], 'tools')
    else:
        args.mpi_dir = os.environ['MPI_DIR']

    fill(template, outfile, **args.__dict__)
    sys.exit(0)
    
