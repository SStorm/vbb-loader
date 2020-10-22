import sys
import csv
import pathlib

from vbb_loader.logging import setup
from vbb_loader.client.db_client import DbClient
from vbb_loader.schema.init import SCHEMA_PREFIX
from vbb_loader.transformers.vbb_transformers import get_transformer

LOGGER = setup.logger(__name__)

BATCH_SIZE = 500


def load(file_to_import: str, url: str, user: str, password: str):
    table = table_from_filename(file_to_import)
    LOGGER.info("Will load file '%s' to table '%s'", file_to_import, table)
    with open(file_to_import, mode='r') as input_file:
        csvfile = csv.DictReader(input_file)
        client = DbClient(url, user, password)
        transformer = get_transformer(table)
        column_names = transformer.column_names(csvfile.fieldnames)
        insert_statement = generate_insert(table, column_names)

        buffer = []
        insert_counter = 0
        for row in csvfile:
            buffer.append(transformer.column_values(row))

            if len(buffer) >= BATCH_SIZE:
                do_insert(client, insert_statement, buffer)
                insert_counter += len(buffer)
                LOGGER.debug('Inserted %d into %s', insert_counter, table)
                buffer = []

        if len(buffer) != 0:
            do_insert(client, insert_statement, buffer)
            insert_counter += len(buffer)
            LOGGER.debug('Inserted %d into %s', insert_counter, table)

        LOGGER.info("Done")


def do_insert(client, insert_statement, rows):
    try:
        all_res = client.cursor().executemany(insert_statement, rows)
        for res in all_res:
            if res['rowcount'] != 1:
                LOGGER.error("Failed inserting rows: %s", rows)
                LOGGER.error("Failure was: %s", all_res)
                raise RuntimeError('Failed inserting batch')
    except:
        LOGGER.error("Failed inserting rows: %s", rows)
        LOGGER.error("Exception was %s",  sys.exc_info()[0])
        raise


def table_from_filename(filename):
    table_name = pathlib.Path(filename).name.split('.')[0]
    return f"{SCHEMA_PREFIX}_{table_name}"


def generate_insert(table_name, columns):
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
    load(file, url, user, password)
