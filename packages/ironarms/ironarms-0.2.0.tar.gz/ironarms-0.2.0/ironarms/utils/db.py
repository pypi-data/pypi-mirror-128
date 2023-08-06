import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.engine.url import URL
from sqlalchemy import exc
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from .helper import get_value


__all__ = [
    "db_url_from_env",
    "db_url_from_settings",
    "create_eng",
    "list_tables",
    "load_syms",
    "get_db_url",
    "add_via_session",
    "create_session",
    "close_session",
    "create_engine",
]


def db_url_from_settings(settings):
    """Creates database url from settings."""
    db_url = settings.get("DATABASE_URL")
    if db_url is not None:
        print("database settings got from settings['DATABASE_URL']")
        return db_url
    db = settings.get("DATABASE")
    if db is not None:
        db_url = URL(**db)
        print("database settings got from settings['DATABASE']")
        return db_url
    print("settings has neither DATABASE_URL nor DATABASE")
    return None


def db_url_from_env():
    """Creates database url from environment variables."""
    db_url = os.environ.get("DATABASE_URL")
    if db_url is not None:
        print("database url got from env DATABASE_URL")
        return db_url

    drivername = "postgresql"
    # environment variable name from bitnami pg docker
    username = os.environ.get("POSTGRESQL_USERNAME")
    password = os.environ.get("POSTGRESQL_PASSWORD")
    host = os.environ.get("POSTGRESQL_HOST") or "pg"
    port = os.environ.get("POSTGRESQL_PORT") or 5432
    database = os.environ.get("POSTGRESQL_DATABASE") or "spider"
    if password is not None and username is not None:
        db_url = URL(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        print("database url got from env POSTGRESQL_*")
        return db_url
    print("env has no information for database url.")
    return None


def get_db_url(settings=None):
    """Gets a database_url from environment, if failed, settings.

    If ``settings`` is ``None``, trying to get the project settings.

    A wrapper over :func:`db_url_from_env` and :func:`db_url_from_settings`.
    """
    v = db_url_from_env()
    if v is not None:
        return v
    if settings is None:
        settings = get_project_settings()
    if settings is None:
        return None
    return db_url_from_settings(settings)


def create_session(database_url, ensure_tables=None):
    """Creates a seesion.

    See Also
    -----------
    pipelines.PGPipeline
    """
    engine = create_engine(database_url)
    for tbl in ensure_tables:
        tbl.__table__.create(bind=engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    return Session()


def close_session(session):
    """Closes session safely.

    See Also
    -----------
    pipelines.PGPipeline

    Raises
    --------
    if failed commit
    """
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_eng(settings=None):
    """Creates a engine by finding database url from environment variables, then
    settings, then project settings.

    Examples
    -----------

    To query table ``chronicle`` from database defined in environment, settings, or
    project settings::

        engine = create_eng()
        df = pd.read_sql_query('SELECT * FROM chronicle LIMIT 10;', con=engine)
        print(df.to_string())

    See Also
    --------
    get_db_url
    """
    db_url = get_db_url()
    return create_engine(db_url)


def list_tables(database_url=None, schema="public"):
    """Returns tables information.

    Parameters
    -----------
    database_url: str, default None
        If None, environment variable ``DATABASE_URL`` would be used.
    schema: str, default ``public``
        If None, all available schemas will be used

    Returns
    ------------
    dict
    """
    database_url = database_url or get_db_url()
    if isinstance(schema, str):
        schema = [schema]

    engine = create_engine(database_url)

    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    if schema is not None:
        schemas = [x for x in schemas if x in schema]

    r = {}
    for sch in schemas:
        for table_name in inspector.get_table_names(schema=sch):
            v = {
                "schema": sch,
                "columns": inspector.get_columns(table_name, schema=sch),
            }
            v["cols"] = len(v["columns"])
            r[table_name] = v

    with engine.connect() as conn:
        for k in r:
            # https://wiki.postgresql.org/wiki/Count_estimate
            if "postgresql" in database_url:
                q = f"SELECT reltuples AS estimate FROM pg_class WHERE relname = '{k}';"
            else:
                q = f"SELECT count(*) FROM {k};"
            n = conn.execute(q).scalars().all()[0]
            r[k]["rows"] = int(n)

    engine.dispose()
    return r


def load_syms(sym_table=None, col_sym="sym", database_url=None):
    """Returns a sorted list of all the unique strings from column ``sym`` in table.

    Parameters
    -----------
    sym_table: str, default None
        If None, environment variable ``SYM_TABLE`` would be used.
        The table should contain column ``sym``.
    col_sym: str, default ``"sym"``
        The column which holds the sym strings
    database_url: str, default None
        If None, environment variable ``DATABASE_URL`` would be used.


    Returns
    ---------
    list
    """
    sym_table = sym_table or get_value("SYM_TABLE") or "hqd_eastmoney"
    database_url = database_url or get_db_url()

    engine = create_engine(database_url)
    with engine.connect() as conn:
        syms = conn.execute(f"SELECT DISTINCT {col_sym} FROM {sym_table};")
    syms = list(syms)
    engine.dispose()
    syms = [x[0] for x in syms]
    syms = sorted(syms)
    return syms


def add_via_session(x, session, raises=True, verbose=True):
    """Adds a row of data into database via session.

    Parameters
    ------------
    x: model instance
    session:
    raises: bool, default True
        If True, raises DropItem if necessary
    verbose: bool, default True

    raises
    ---------
    DropItem, if failed and raises is True
    """
    try:
        session.add(x)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        if e.orig.pgcode == "23505":
            if verbose:
                print("item exists in postgres already.")
        else:
            if verbose:
                print(f"Unexpected exception: {e}")
        if raises:
            raise DropItem("Exists already")
    except Exception as e:
        session.rollback()
        if verbose:
            print(f"Unexpected exception: {e}")
        if raises:
            raise DropItem("Unexpected")
