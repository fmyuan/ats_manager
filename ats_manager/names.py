import os

_amanzi_url_template = 'https://github.com/amanzi/{}.git'
amanzi_url = _amanzi_url_template.format('amanzi')
ats_url = _amanzi_url_template.format('ats')
ats_regression_tests_url = _amanzi_url_template.format('ats-regression-tests')
ats_demos_url = _amanzi_url_template.format('ats-demos')
valid_build_types = ['debug', 'opt', 'relwithdebinfo']
ats_submodule = 'src/physics/ats'


def filename(amanzi_name, ats_name, build_type, prefix=None):
    """Returns a unique filename for identifying installations."""
    if ats_name is None:
        if prefix is None:
            prefix = 'amanzi'
        return '{}/{}/{}'.format(prefix,amanzi_name.replace('/', '-'),build_type)
    else:
        if prefix is None:
            prefix = 'ats'
        if ats_name == amanzi_name:
            return '{}/{}/{}'.format(prefix,ats_name.replace('/', '-'),build_type)
        else:
            return '{}/{}-{}/{}'.format(prefix,amanzi_name.replace('/', '-'),
                                        ats_name.replace('/', '-'),build_type)

        
def split_filename(name):
    """Splits a unique filename into its components."""
    split = name.split('/')
    if split[0] == 'amanzi':
        return split[1],None,split[2]
    elif split[0] == 'ats':
        names = split[1].split('-')
        if len(names) == 1:
            return split[1], split[1], split[2]
        else:
            return names[0], names[1], split[2]

        
def unique_string(amanzi_name, ats_name, build_type):
    """Creates a unique (non-filename) string to identify an installation."""
    return filename(amanzi_name,ats_name,build_type).replace('/','-')

def tpls_name(name):
    name_split = split_filename(name)
    assert(len(name_split) is 3)
    if name_split[1] is None:
        inner_name = name_split[0]
    else:
        inner_name = name_split[0]+'-'+name_split[1]
    return '/'.join(['amanzi-tpls',inner_name, name_split[2]])

# paths to useful places
def amanzi_src_dir(name):
    name_trip = name.split('/')
    return os.path.join(os.environ['ATS_BASE'], name_trip[0], 'repos', name_trip[1])

def amanzi_install_dir(name):
    name_trip = name.split('/')
    return os.path.join(os.environ['ATS_BASE'], name_trip[0], 'install-'+name_trip[1], name_trip[2])

def amanzi_build_dir(name):
    name_trip = name.split('/')
    return os.path.join(os.environ['ATS_BASE'], name_trip[0], 'build-'+name_trip[1], name_trip[2])

def ats_src_dir(name):
    return os.path.join(amanzi_src_dir(name), ats_submodule)

def ats_regression_tests_dir(name):
    name_trip = name.split('/')
    assert(name_trip[0] == 'ats')
    return os.path.join(os.environ['ATS_BASE'], 'testing', 'ats-regression-tests', name_trip[1], name_trip[2])

def tpls_build_dir(name):
    tpls_trip = name.split('/')
    return os.path.join(os.environ['ATS_BASE'], tpls_trip[0], 'build-'+tpls_trip[1], tpls_trip[2])

def tpls_install_dir(name):
    tpls_trip = name.split('/')
    return os.path.join(os.environ['ATS_BASE'], tpls_trip[0], 'install-'+tpls_trip[1], tpls_trip[2])

def modulefile_path(name):
    return os.path.join(os.environ['ATS_BASE'], 'modulefiles', name)

def tools_mpi_dir(vendor):
    return os.path.join(os.environ['ATS_BASE'], 'tools', 'install-{}'.format(vendor))


