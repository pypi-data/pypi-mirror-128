import os, hashlib, subprocess, shlex, uuid, re
from .commandlineopt import NoTracebackError

__all__ = ["md5sum_of_file", "check_file_presence", "checksum_of_file", "random_folder",
           "run_cmd", "mask_chars", "unmask_chars"]

def check_file_presence(input_file, descriptor='input_file', exception_raised=NoTracebackError):
    """Check if file exists. If it doesn't, raises a IOError exception

    Parameters
    ----------
    input_file : str
        string of file to check, any relative or absolute path

    descriptor : str
        used for meaningful error message if file is absent

    exception_raised : class
        Exception class to be raised

    Returns
    -------
    None
        None
    """
    if not input_file or not os.path.isfile(input_file):
        raise(exception_raised(f"ERROR {descriptor}: {input_file} not defined or not found. Run with option -h for help."))
    
def md5sum_of_file(filename, chunksize=4096):
    """Gets md5sum of content of a file

    Parameters
    ----------
    filename : str
        file to be read

    Returns
    -------    
    md5sum : str
        md5sum of file
    """    
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(chunksize), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def checksum_of_file(filename):
    """ Gets checksum of content of a file, using program 'sum'

    Parameters
    ----------
    filename : str
        file to be read

    Returns
    -------
    (sum1, sum2) : (int, int)
        checksum of file
    """        
    p = subprocess.run(['sum', filename],
                       capture_output=True,
                       check=True)
    int1, int2=map(int, p.stdout.decode().strip().split())
    return( (int1, int2) )

def random_folder(parent_folder='./', mkdir=True):
    """Generate a random folder name, create it inside parent_folder, and return the path to it

    Parameters
    ----------
    parent_folder : str
        folder inside which the random_folder is desired

    mkdir : bool
        whether the random folder should be created (by default: True)

    Returns
    -------
    rnd_folder : str
        path to newly created random folder (whose name will look like 57eb3f2416bc4c5d9d34a17751c97362)

    """
    parent_folder=parent_folder.rstrip('/')+'/'
    if not os.path.isdir(parent_folder):
        raise Exception(f'random folder ERROR the parent folder does not exist: {parent_folder}')
    
    random_name=uuid.uuid4().hex # style: 57eb3f2416bc4c5d9d34a17751c97362
    random_folder_created=parent_folder + random_name
    
    if mkdir:
        os.mkdir( random_folder_created )
        
    return random_folder_created

def run_cmd(cmd, err_crash=True, **keyargs):
    """Utility function to run bash commands.

    This function wraps subprocess.run for its most common usage
    (according to easyterm developer, at least!).
    You can provide any of subprocess.run options to modify its behaviour.
    
    The input is the string of the command you would run in a terminal.
    It returns a class subprocess.CompletedProcess instance with attributes
    returncode, stdout (coded as text, joining stdout and stderr).

    Parameters
    ----------
    cmd : str
        command, just as you would run in a terminal

    err_crash : bool, optional
        if err_crash==True (default) and the process fails (exitcode!=0), an exception is raised
        including an informative message.

    **kwargs
        keyword arguments that will be passed to subprocess.run

    Returns
    -------
    proc : subprocess.CompletedProcess
       completed process, with attributes returncode, stdout, and others (see subprocess.run)

    Note
    ----
    By default, stdout and stderr are joined in the stdout property of the returned object.
    To separate them instead, use stderr=subprocess.PIPE

    """
    default_keyargs={'stdout':subprocess.PIPE, 'stderr':subprocess.STDOUT, 'text':True}
    for k, v in default_keyargs.items():
        keyargs.setdefault(k, v)
    try:
        p=subprocess.run(shlex.split(cmd), **keyargs)
        if err_crash and p.returncode!=0:
            raise Exception(f'\nWhile running command= {cmd}\nThere was ERROR= {p.stdout}')

    except FileNotFoundError:
        if err_crash:
            raise Exception(f'\nWhile running command= {cmd}\nThere was ERROR= FileNotFoundError, '
                            f'which means that the command was not found!') from None

    return p


def _mask_replace(match):
    return '{ch'+str(ord(match.group()))+'}'
def _unmask_replace(match):
    return chr(int(match.group(1)))

def mask_chars(astring):
    """Replace potentially problematic characters in a string so that it can be used as filename.

    All characters which are not alphanumeric (e.g. :/?@#$_) are replaced to '{chN}', where N is 
    their ASCII code. Also, spaces are converted to underscores. Note that underscores originally 
    present in input string are converted to {ch95}.

    You may do the reverse (get back the original unmasked string) using function unmask_chars.

    Parameters
    ----------
    astring : str
        input string to be masked

    Returns
    -------
    mstring : str
        string with potentially problematic characters masked
    
    Examples
    --------
    >>> mask_chars('some species name')
    'some_species_name'

    >>> mask_chars('string containing /')
    'string_containing_{ch47}'

    >>> mask_chars('lots of #strange $characters here to @mask !')
    'lots_of_{ch35}strange_{ch36}characters_here_to_{ch64}mask_{ch33}'

    See also
    --------
    unmask_chars
    """    
    return re.sub(r'[^a-zA-Z0-9 ]', _mask_replace, astring).replace(' ', '_')

def unmask_chars(mstring):
    """Reverses function mask_chars.

    Substrings matching '{chN}', where N is an integer, are converted to their original 
    value before masking (the ascii character identified by that integer).    
    Also, underscores are converted to spaces.

    Parameters
    ----------
    mstring : str
        masked input string to be unmasked

    Returns
    -------
    ustring : str
        unmasked string, i.e. the original input fed to mask_chars in the first place.

    Examples
    --------

    >>> unmask_chars('some_simple_string')
    'some simple string'

    >>> unmask_chars('lots_of_{ch35}strange_{ch36}characters_here_to_{ch64}mask_{ch33}')
    'lots of #strange $characters here to @mask !'

    See also
    --------
    mask_chars
    """
    return re.sub(r'\{ch(\d+)\}', _unmask_replace,  mstring.replace('_', ' ') )

