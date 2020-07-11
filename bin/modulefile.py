import argparse
import sys,os

def fill(file_in, file_out, substitutions):
    print("Got substitutions:")
    for s in substitutions:
        print("{}: {}".format(s,substitutions[s]))
    with open(file_in,'r') as fin:
        template = '\n'.join(fin.readlines())

    modfile = template.format(**substitutions)
    with open(file_out, 'w') as fout:
        fout.write(modfile)
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
    parser.add_argument('--tools-mpi',
                        action='store_true',
                        help='Use bootstrap MPI')
    return parser



if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()

    # set the template file
    if args.ats is None:
        template = os.path.join(os.environ['ATS_BASE'], 'bin', 'templates',
                                'amanzi_modulefile.template')
    else:
        template = os.path.join(os.environ['ATS_BASE'], 'bin', 'templates',
                                'ats_modulefile.template')

    # set the output file
    outfile_list = [os.environ['ATS_BASE'],'modulefiles']
    if args.ats is None:
        outfile_list.append('amanzi')
        outfile_list.append(args.amanzi)
    else:
        outfile_list.append('ats')
        outfile_list.append('{}-{}'.format(args.amanzi,args.ats))

    outfile_dir = os.path.join(*outfile_list)
    os.makedirs(outfile_dir, exist_ok=True)
    outfile_list.append(args.build_type)
    outfile = os.path.join(*outfile_list)

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

    fill(template, outfile, vars(args))
    sys.exit(0)
    
