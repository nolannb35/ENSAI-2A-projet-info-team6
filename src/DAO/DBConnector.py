import os
from typing import Literal, Optional, Union

import psycopg2
from psycopg2.extras import RealDictCursor

from src.utils.singleton import Singleton


class DBConnector(metaclass=Singleton):
    """Database connection manager implementing the Singleton pattern.

    Only one connection to the PostgreSQL database is opened and shared
    by the whole application (DAO classes use DBConnector().connection).

    The connection is opened the first time it is needed, and reopened
    automatically if it has been closed.
    """

    def __init__(self, config=None):
        """Read the connection parameters.
        Args:
            config (dict, optional): host, port, database, user, password, schema.
                If None, the POSTGRES_* environment variables are used.
        Raises:
            KeyError: if a required parameter / environment variable is missing
        """
        if config is not None:
            self.host = config["host"]
            self.port = config["port"]
            self.database = config["database"]
            self.user = config["user"]
            self.password = config["password"]
            self.schema = config["schema"]
        else:
            self.host = os.environ["POSTGRES_HOST"]
            self.port = os.environ["POSTGRES_PORT"]
            self.database = os.environ["POSTGRES_DATABASE"]
            self.user = os.environ["POSTGRES_USER"]
            self.password = os.environ["POSTGRES_PASSWORD"]
            self.schema = os.environ["POSTGRES_SCHEMA"]

        self.__connection = None

    @property
    def connection(self):
        """Provide access to the shared database connection.

        Usage in a DAO:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(...)

        `with connection` commits the transaction if everything went well,
        and rolls it back if an exception is raised (the connection stays open).

        Returns:
            psycopg2 connection (rows are returned as dict thanks to RealDictCursor)
        """
        if self.__connection is None or self.__connection.closed:
            self.__connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                options=f"-c search_path={self.schema}",
                cursor_factory=RealDictCursor,
            )
        return self.__connection

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "one",
    ):
        """Execute a query and return one row or all rows.
        Kept for the classes that do not use DBConnector().connection directly
        (UserRepo...).
        """
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, data)
                    if return_type == "one":
                        return cursor.fetchone()
                    if return_type == "all":
                        return cursor.fetchall()
        except Exception as e:
            print("ERROR")
            print(e)
            raise e