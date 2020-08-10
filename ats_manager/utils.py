import os,stat
import subprocess
import logging
import ats_manager.names as names


def script_name(prefix, name):
    return '{}-{}.sh'.format(prefix,names.unique_string(*names.split_filename(name)))

def run_cmd(prefix, name, cmd):
    script = script_name(prefix, name)
    outfile = os.path.join(os.environ['ATS_BASE'], 'scripts', script)
    with open(outfile,'w') as fid:
        fid.write(cmd)
    os.chmod(outfile, stat.S_IRWXU) # owner r/w/x
    return run_script(prefix, name)

def run_script(prefix, name):
    script = script_name(prefix, name)
    outfile = os.path.join(os.environ['ATS_BASE'], 'scripts', script)
    logging.info('Running {}'.format(script))
    logging.info('  file  {}'.format(outfile))
    assert(os.path.isfile(outfile))
    out = subprocess.run(outfile, capture_output=True, shell=True)
    logging.info(out.stdout.decode('utf-8'))
    logging.error(out.stderr.decode('utf-8'))
    return out.returncode

