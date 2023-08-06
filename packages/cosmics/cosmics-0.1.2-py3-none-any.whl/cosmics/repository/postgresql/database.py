import logging
from typing import Any
from typing import Optional
from typing import Union

import psycopg2.extensions
import psycopg2.extras
from psycopg2 import sql

from . import _query_builder as query_builder
from cosmics.repository import database

logger = logging.getLogger(__name__)


class Client(database.AbstractClient):
    """Client to connect to a Postgresql database and read from/write to it."""

    _connection: Optional[psycopg2.extensions.connection] = None

    def __init__(self, user: str, password: str, host: str, port: int, database: str):
        """Initialize SQL Client.

        Parameters
        ----------
        user : str
            Database user name.
        password : str
            Password for given user.
        host : str
            IP address or hostname of database host.
        port : int
            Port at which the database accepts connections.
        database : str
            Name of the database.

        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._connection = None

    def __enter__(self):
        """Return instance when entering context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection on exit."""
        if all(param is None for param in [exc_type, exc_val, exc_tb]):
            # Transaction completed without any errors
            self.__del__(commit=True)
            return
        self.__del__(commit=False)

    def __del__(self, commit: bool = False):
        """Close database connection on deletion."""
        if self._connection is not None:
            if commit:
                self._connection.commit()
            self._connection.close()
            self._connection = None

    @property
    def credentials(self) -> dict[str, Union[str, int]]:
        """Return username, password, host, port, and dbname as dict.

        Returns
        -------
        dict[str, str | int]

        """
        return {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": self.database,
        }

    @property
    def connection(self) -> psycopg2.extensions.connection:
        """Create SQL database connection.

        Returns
        -------
        psycopg2.extensions.connection

        """
        if self._connection is None:
            self._connection = psycopg2.connect(**self.credentials)
            logger.debug(
                "Connected to database %s as user %s", self.database, self.user
            )
        return self._connection

    def _insert(self, target: str, data: database.Info) -> None:
        """Insert row into table.

        Parameters
        ----------
        target : str
            Table name.
        data : dict[str, Any]
            Data to insert.

        """
        filtered = self._filter_non_existing_columns(table=target, data=data)
        query = query_builder.create_insert_query(table=target, data=filtered)
        with self.connection.cursor() as cursor:
            self._execute_query(cursor, query=query)

    def insert_and_return_row_id(self, target: str, data: database.Info) -> int:
        """Insert row into table and return the inserted row's ID.

        Parameters
        ----------
        target : str
            Table name.
        data : dict[str, Any]
            Data to insert.

        Returns
        -------
        int
            ID of inserted row.

        """
        filtered = self._filter_non_existing_columns(table=target, data=data)
        query = query_builder.create_insert_query(table=target, data=filtered)
        with self.connection.cursor() as cursor:
            self._execute_query(cursor, query=query)
            return cursor.lastrowid

    def _select(
        self,
        target: str,
        where: Optional[database.Info] = None,
    ) -> list[dict[str, Any]]:
        """Select columns from table.

        Parameters
        ----------
        target : str
            View or table name.
        where : dict[str, Any]
            Criteria which row(s) to update.

        Returns
        -------
        list[dict[str, Any]]
            All matching rows.

        """
        query = query_builder.create_select_query(table=target)
        if where is not None:
            filtered = self._filter_non_existing_columns(table=target, data=where)
            query += query_builder.create_where_clause(filtered)
        query += sql.SQL(";")
        with self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cursor:
            self._execute_query(cursor, query=query)
            return [dict(row) for row in cursor.fetchall()]

    def _update(
        self,
        target: str,
        data: database.Info,
        where: database.Info,
    ) -> None:
        """Update entry.

        Parameters
        ----------
        target : str
            Table name.
        data : dict[str, Any]
            Columns to update.
        where : dict
            Current details.
            Used to find matching row(s) in a table.

        """
        data_filtered = self._filter_non_existing_columns(table=target, data=data)
        where_filtered = self._filter_non_existing_columns(table=target, data=where)
        query = query_builder.create_update_query(table=target, data=data_filtered)
        query += query_builder.create_where_clause(where_filtered)
        query += sql.SQL(";")
        with self.connection.cursor() as cursor:
            self._execute_query(cursor, query=query)

    def _delete(self, target: str, where: database.Info) -> None:
        """Delete entry.

        Parameters
        ----------
        target : str
            Table from which to delete the row.
        where : dict[str, Any]
            Criteria for matching rows to delete.

        """
        filtered = self._filter_non_existing_columns(table=target, data=where)
        query = query_builder.create_delete_query(table=target)
        query += query_builder.create_where_clause(filtered)
        query += sql.SQL(";")
        with self.connection.cursor() as cursor:
            self._execute_query(cursor, query=query)

    def _execute_query(
        self, cursor: psycopg2.extras._cursor, query: sql.Composed
    ) -> None:
        logger.debug("Executing query %s", query.as_string(self.connection))
        cursor.execute(query)

    def _filter_non_existing_columns(
        self, table: str, data: database.Info, schema: Optional[str] = None
    ) -> database.Info:
        table_columns = self._get_table_columns(table=table, schema=schema)
        return {
            column: value for column, value in data.items() if column in table_columns
        }

    def _get_table_columns(
        self, table: str, schema: Optional[str] = None
    ) -> list[database.Info]:
        columns = self._get_table_columns_and_data_types(table=table, schema=schema)
        return [column["column_name"] for column in columns]

    def _get_table_columns_and_data_types(
        self, table: str, schema: Optional[str] = None
    ) -> list[database.Info]:
        """Return all table columns and their data types.

        Returns
        -------
        list[dict]
            Each dict contains the `column_name` and `data_type`.
            I.e. for a table with a column named `test_column` of type `TEXT`,
            the returned list looks as follows:
            `[{'column_name': 'test_column', 'data_type': 'text'}]`

        """
        with self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cursor:
            query = query_builder.create_select_columns_and_types_query(
                table=table, schema=schema
            )
            self._execute_query(cursor, query=query)
            return [dict(row) for row in cursor.fetchall()]
