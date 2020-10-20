# Roman's Crate VBB schema loader

## General principles

- Attempting to use PGSQL compatibility as much as possible, w/o doing anything crate-specific
- Using Python 3.8.2 (others might work too) in .python-version (pyenv)


## Work log

Attempted to use yoyo (for db init) with the psycopg2 package to init DB schema that way - no luck. 
Always fails with with error like:

    psycopg2.errors.InternalError_: SQLParseException: line 1:1: mismatched input 'SAVEPOINT' expecting {'SELECT', 'DEALLOCATE', 'CREATE', 'ALTER', 'KILL', 'BEGIN', 'COMMIT', 'ANALYZE', 'DISCARD', 'EXPLAIN', 'SHOW', 'OPTIMIZE', 'REFRESH', 'RESTORE', 'DROP', 'INSERT', 'VALUES', 'DELETE', 'UPDATE', 'SET', 'RESET', 'COPY', 'GRANT', 'DENY', 'REVOKE'}

At least upon first attempt, Postgres compatibility is not straightforward. 

Next attempt - alembic / sqlalchemy. The crate python driver says it's sqlalchemy compatible, but will it work with alembic??

After some basic setup, running:

    VBB_DB_URL="crate://crate@localhost" alembic upgrade head

Sadly no such luck:

    ... snip ...
    File "/home/romanas/work/crate/vbb-loader/venv/lib/python3.8/site-packages/alembic/runtime/environment.py", line 816, in configure
        self._migration_context = MigrationContext.configure(
    File "/home/romanas/work/crate/vbb-loader/venv/lib/python3.8/site-packages/alembic/runtime/migration.py", line 220, in configure
        return MigrationContext(dialect, connection, opts, environment_context)
    File "/home/romanas/work/crate/vbb-loader/venv/lib/python3.8/site-packages/alembic/runtime/migration.py", line 147, in __init__
        self.impl = ddl.DefaultImpl.get_by_dialect(dialect)(
    File "/home/romanas/work/crate/vbb-loader/venv/lib/python3.8/site-packages/alembic/ddl/impl.py", line 78, in get_by_dialect
        return _impls[dialect.name]
    KeyError: 'crate'

So even though alembic manages to detect the correct db type to use (crate) 
it has no dialect for crate and there doesn't seem to be an easy way to override that.

OK, at this point I have a feeling that nice DB migrations aren't going to work for me :(