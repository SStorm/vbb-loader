import sys
from os import listdir
from os.path import isfile, join

from .load_file import TableLoader
from vbb_loader.transformers.vbb_transformers import TableNotSupportedException
from vbb_loader.logging.setup import logger

LOGGER = logger(__name__)

if __name__ == '__main__':
    # Parse args
    if len(sys.argv) != 5:
        print("Usage: ")
        print("./load_dir.py [dir] [db-connection-url] [user] [password]")
        exit(1)

    dir = sys.argv[1]
    url = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]

    files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.txt')]
    for f in files:
        try:
            TableLoader(join(dir, f), url, user, password).load()
        except TableNotSupportedException:
            LOGGER.warning(f'No such table for file {f}')

    LOGGER.info('Done')
