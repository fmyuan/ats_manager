import argparse
import sys,os
import logging

import ats_manager.names as names

def fill_template(file_in, file_out, substitutions):
    """Fills a python template file and writes it to disk."""
    logging.info("Writing template: {}".format(file_in))
    logging.info(" to: {}".format(file_out))
    logging.info(" using substitutions:")
    for key,val in substitutions.items():
        logging.info("  {} : {}".format(key,val))

    with open(file_in,'r') as fin:
        template = fin.read()
    modfile = template.format(**substitutions)
    with open(file_out, 'w') as fout:
        fout.write(modfile)
    return


def amanzi_modulefile_args(name, repo_name, tpls_name, **kwargs):
    temp_pars = dict()
    temp_pars.update(**kwargs)
    temp_pars['amanzi'] = name
    temp_pars['tpls_dir'] = names.tpls_install_dir(tpls_name)
    temp_pars['tpls_build_dir'] = names.tpls_build_dir(tpls_name)
    temp_pars['amanzi_dir'] = names.amanzi_install_dir(name)
    temp_pars['amanzi_build_dir'] = names.amanzi_build_dir(name)
    temp_pars['amanzi_src_dir'] = names.amanzi_src_dir(repo_name)
    return temp_pars
                           
def ats_modulefile_args(name, repo_name, tpls_name, **kwargs):
    temp_pars = amanzi_modulefile_args(name, repo_name, tpls_name, **kwargs)
    temp_pars['ats'] = name
    temp_pars['ats_src_dir'] = names.ats_src_dir(repo_name)
    temp_pars['ats_regression_tests_dir'] = names.ats_regression_tests_dir(name)
    return temp_pars
    
def template_path(ats=False):
    """Returns the name of the template to be filled."""
    if ats:
        return os.path.join(os.environ['ATS_BASE'],'ats_manager','share','templates','ats_modulefile.template')
    else:
        return os.path.join(os.environ['ATS_BASE'],'ats_manager','share','templates','amanzi_modulefile.template')


def create_modulefile(name, repo_name, tpls_name, **kwargs):
    """Sets up the name of the modulefile to be created.  Note this also
    creates the subdirectory containing that file, if needed."""
    outfile = names.modulefile_path(name)
    outfile_dir = os.path.join(*os.path.split(outfile)[:-1])
    os.makedirs(outfile_dir, exist_ok=True)

    name_trip = name.split('/')
    if name_trip[0] == 'ats':
        temp_pars = ats_modulefile_args(name, repo_name, tpls_name, **kwargs)
        template = template_path(True)
    else:
        temp_pars = amanzi_modulefile_args(name, repo_name, tpls_name, **kwargs)
        template = template_path(False)

    fill_template(template, outfile, temp_pars)
    return temp_pars
