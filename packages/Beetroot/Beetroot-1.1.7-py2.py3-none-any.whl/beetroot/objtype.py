#Dependency function of like almost every class
"""I originally wanted this to be just for objtype(),
but now I have other global functions and nowhere to put them,
and changing the name would've been too hard with my
one billion files."""

import os
import sys

from .exception import *

def objtype(obj):
    return str(type(obj))[8:-2]

class suppress(object):
    """Forcibly suppress stdout and stderr, however
    errors and stack traces will still show"""
    def __init__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup = sys.stdout.fileno()
        self.old_stderr_fileno_undup = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup(sys.stdout.fileno())
        self.old_stderr_fileno = os.dup(sys.stderr.fileno())

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2(self.outnull_file.fileno(), self.old_stdout_fileno_undup)
        os.dup2(self.errnull_file.fileno(), self.old_stderr_fileno_undup)

        sys.stdout = self.outnull_file
        sys.stderr = self.errnull_file  
        return self

    def __exit__(self, *args, **kwargs):        
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2(self.old_stdout_fileno, self.old_stdout_fileno_undup)
        os.dup2(self.old_stderr_fileno, self.old_stderr_fileno_undup)

        os.close(self.old_stdout_fileno)
        os.close(self.old_stderr_fileno)

        self.outnull_file.close()
        self.errnull_file.close()