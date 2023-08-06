from typing import Optional

from psycopg2 import sql


def create_insert_query(
    table: str,
    data: dict,
    return_output: bool = False,
) -> sql.Composed:
    """Create an SQL INSERT query for table from given kwargs.

    Parameters
    ----------
    table : str
        Name of the table.
    data : dict
        Data to insert.
    return_output : bool, optional
        Whether to return inserted row(s).
        Defaults to `False`.

    Returns
    -------
    psycopg2.sql.Composed
        Composed query.

    """
    query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
        table=sql.Identifier(table),
        columns=sql.SQL(", ").join([sql.Identifier(key) for key in data.keys()]),
        values=sql.SQL(", ").join([sql.Literal(value) for value in data.values()]),
    )
    if return_output:
        query += sql.SQL(" RETURNING *")
    query += sql.SQL(";")
    return query


def create_select_query(table: str) -> sql.Composed:
    """Create SQL SELECT query for table.

    The kwargs enable finding all rows matching the defined criteria
    If kwargs are not passed, the entire table will be selected.

    Parameters
    ----------
    table : str
        Name of the table.

    Returns
    -------
    psycopg2.sql.Composed
        Composed query.

    """
    query = sql.SQL("SELECT * FROM {table} ").format(table=sql.Identifier(table))
    return query


def create_update_query(table: str, data: dict) -> sql.Composed:
    """Create an SQL UPDATE query for given table.

    Parameters
    ----------
    table : str
        Table into which to insert.
    data: dict
        Data to insert.

    Returns
    -------
    psycopg2.sql.Composed

    """
    query = sql.SQL("UPDATE {table} SET ").format(table=sql.Identifier(table))

    for i, (key, value) in enumerate(data.items()):
        query += sql.SQL(" {key} = {value} ").format(
            key=sql.Identifier(key),
            value=sql.Literal(value),
        )
        if len(data) > 1 and i < len(data) - 1:
            query += sql.SQL(", ")
    return query


def create_delete_query(table: str) -> sql.Composed:
    """Create an SQL DELETE query for given table.

    Parameters
    ----------
    table : str

    Returns
    -------
    psycopg2.sql.Composed

    """
    return sql.SQL("DELETE FROM {table} ").format(table=sql.Identifier(table))


def create_where_clause(where: dict) -> sql.Composed:
    """Create an SQL WHERE clause from given kwargs.

    Returns
    -------
    psycopg2.sql.Composed
        Composed clause with `WHERE` and kwargs.

    """
    query = sql.SQL(" WHERE ")
    for i, (key, value) in enumerate(where.items()):
        if isinstance(value, list) and all(isinstance(val, int) for val in value):
            # TODO: implement respecting data type of arrays
            # currently, the only integer arrays are BIGINT
            logical_string = " {column} {operator} {value}::bigint[] "
        else:
            logical_string = " {column} {operator} {value} "
        query += sql.SQL(logical_string).format(
            column=sql.Identifier(key),
            operator=sql.SQL("=") if value is not None else sql.SQL("IS"),
            value=sql.Literal(value),
        )
        if len(where) > 1 and i < len(where) - 1:
            query += sql.SQL(" AND ")
    return query


def create_select_columns_and_types_query(
    table: str, schema: Optional[str]
) -> sql.Composed:
    """Return a select query for columns and data types of a table."""
    query = sql.SQL(
        "SELECT column_name, data_type FROM information_schema.columns WHERE "
    )
    query += sql.SQL(" table_name = {table} ").format(table=sql.Literal(table))
    if schema is not None:
        query += sql.SQL(" AND table_schema = {schema}").format(
            schema=sql.Literal(schema)
        )
    query += sql.SQL(";")
    return query
