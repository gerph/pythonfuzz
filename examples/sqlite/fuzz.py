import os
import sqlite3
import sys

from pythonfuzz.main import PythonFuzz


here = os.path.dirname(__file__)


@PythonFuzz
def fuzz(buf):
    try:
        conn = sqlite3.connect(':memory:')
        string = buf.decode("utf-8")
        c = conn.cursor()
        c.execute(string)
    except (UnicodeDecodeError, sqlite3.DatabaseError):
        pass


if __name__ == '__main__':
    # Forcibly add our SQL words list to those that we'll use as a dictionary
    sys.argv.extend(['--dict', os.path.join(here, 'words.txt')])
    # Restrict to remove the binary type operations
    sys.argv.extend(['--mutator-filter', '!byte !short !long !longlong !bit'])
    import random
    random.seed(56)
    fuzz()
