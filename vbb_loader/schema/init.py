import sys
import pathlib

from vbb_loader.logging import setup
from vbb_loader.client.db_client import DbClient

LOGGER = setup.logger(__name__)

SCHEMA_PREFIX = 'vbb'


# Note: ability to connect to multiple nodes has been de-scoped
def migrate(db_url: str, username: str, password: str):
    client = DbClient(db_url, username, password)

    with open(pathlib.Path(__file__).parent / 'schema.sql', mode='r') as file:
        sql = file.read()
        cursor = client.cursor()

        # This is a bit naive, however I couldn't figure out a way of executing the whole SQL against crate
        for statement in sql.split(';'):
            statement = statement.strip()
            if len(statement) < 1:
                continue
            LOGGER.debug("Will execute '%s'", statement)
            cursor.execute(statement)


if __name__ == '__main__':
    # Parse args
    if len(sys.argv) != 4:
        print("Usage: ")
        print("./init.py [db-connection-url] [user] [password]")
        exit(1)

    url = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    migrate(url, user, password)
