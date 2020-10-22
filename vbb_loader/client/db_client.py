from crate import client
from vbb_loader.logging import setup

LOGGER = setup.logger(__name__)


class DbClient:

    def __init__(self, db_url: str, username: str, password: str):
        LOGGER.info("Will connect to CrateDB at '%s' ...", db_url)
        conn = client.connect(db_url, username=username, password=password)
        self._cursor = conn.cursor()
        self._cursor.execute("SELECT 1")
        LOGGER.info("Success")

    def cursor(self):
        return self._cursor

