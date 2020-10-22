import sys
import csv
import pathlib

from vbb_loader.logging import setup
from vbb_loader.client.db_client import DbClient
from vbb_loader.schema.init import SCHEMA_PREFIX
from vbb_loader.transformers.vbb_transformers import get_transformer

LOGGER = setup.logger('TableLoader')

BATCH_SIZE = 1000


class TableLoader:
    def __init__(self, file_to_import: str, url: str, user: str, password: str, truncate=False):
        self.file_to_import = file_to_import
        self.table = self.__table_from_filename(file_to_import)
        self.transformer = get_transformer(self.table)
        self.client = DbClient(url, user, password)
        self.counter = 0
        self.insert_statement = ''
        self.truncate = truncate

    def load(self):
        if self.counter != 0:
            raise RuntimeError('This instance has already finished inserting')

        if self.truncate:
            LOGGER.info(f'Truncation of table {self.table} requested')
            self.client.cursor().execute(f'DELETE FROM {self.table}')

        LOGGER.info("Will load file '%s' to table '%s'", self.file_to_import, self.table)
        with open(self.file_to_import, mode='r') as input_file:
            csvfile = csv.DictReader(input_file)
            column_names = self.transformer.column_names(csvfile.fieldnames)
            self.insert_statement = self.__generate_insert(self.table, column_names)

            buffer = []
            for row in csvfile:
                val = self.transformer.column_values(row)
                if val is not None:
                    buffer.append(val)
                self.__flush_batch_if_required(buffer)

            # Notify the transformer about the file finishing. For stateful transformers this is a way to get them to flush the remaining content.
            val = self.transformer.eof()
            if val is not None:
                buffer.append(val)
            self.__flush_batch_if_required(buffer, force=True)

            LOGGER.info(f"Loaded {self.counter} rows")

    def __flush_batch_if_required(self, buffer: list, force=False):
        if len(buffer) >= BATCH_SIZE or (force and len(buffer) > 0):
            self.__do_insert(self.client, self.insert_statement, buffer)
            self.counter += len(buffer)
            LOGGER.debug('Inserted %d into %s', self.counter, self.table)
            buffer.clear()

    @staticmethod
    def __do_insert(client, insert_statement, rows):
        try:
            all_res = client.cursor().executemany(insert_statement, rows)
            for res in all_res:
                if res['rowcount'] != 1:
                    LOGGER.error("Failed inserting rows: %s", rows)
                    LOGGER.error("Failure was: %s", all_res)
                    raise RuntimeError('Failed inserting batch')
        except:
            LOGGER.error("Failed inserting rows: %s", rows)
            LOGGER.error("Exception was %s", sys.exc_info()[0])
            raise

    @staticmethod
    def __table_from_filename( filename):
        table_name = pathlib.Path(filename).name.split('.')[0]
        return f"{SCHEMA_PREFIX}_{table_name}"

    @staticmethod
    def __generate_insert( table_name, columns):
        col_list = ','.join(columns)
        placeholders = ','.join(['?' for _ in columns])
        return f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})"


if __name__ == '__main__':
    # Parse args
    if len(sys.argv) != 5:
        print("Usage: ")
        print("./load_file.py [file] [db-connection-url] [user] [password]")
        exit(1)

    file = sys.argv[1]
    url = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    TableLoader(file, url, user, password, truncate=True).load()
