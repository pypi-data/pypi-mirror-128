from airflow_commons.logger import LOGGER
from airflow_commons.utils.mysql.mysql_utils import upsert, get_db_engine
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.utils.mysql.sql_utils import get_delete_sql
from airflow_commons.utils.mysql.sql_utils import get_select_all_sql
from airflow_commons.utils.mysql.sql_utils import get_row_count_sql


def write_to_mysql(
    username: str,
    password: str,
    host: str,
    db_name: str,
    values: dict,
    chunk_size: int,
    table_name: str,
):
    """

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param values: values to write into database
    :param chunk_size: data size to upload at a time
    :param table_name: database table name to write
    :return:
    """
    engine = get_db_engine(username, password, host, db_name)
    chunks = [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]
    LOGGER.info(f"Chunk size is {chunk_size}.")
    with engine.connect() as conn:
        i = 0
        for chunk in chunks:
            i += 1
            upsert(values=chunk, conn=conn, table_name=table_name)
            LOGGER.info(f"Chunk {i} uploaded")
    LOGGER.info("Data uploaded to MySql.")


def delete(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str,
    where_statement_params: dict = None,
):
    """
    Runs a delete query on given table, and removes rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: table name
    :param where_statement_file: relative location of where statement sql file
    :param where_statement_params: parameters of where statements
    """
    engine = get_db_engine(username, password, host, db_name)
    connection = engine.raw_connection()
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_delete_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    LOGGER.info(f"The below sql statement is executed \n {sql}")


def select_all(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str,
    where_statement_params: dict = None,
):
    """
    Runs a select query on given table and returns the rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: database table name
    :param where_statement_params: relative location of where statement sql file
    :param where_statement_file: parameters of where statements
    :return: iterable ResultProxy object that stores results of the select query
    """
    engine = get_db_engine(username, password, host, db_name)
    connection = engine.raw_connection()
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_select_all_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    LOGGER.info(f"The below sql statement is executed \n {sql}")
    LOGGER.info(f"Number of records retrieved = {str(len(result))}")
    return result


def get_row_count(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str = None,
    where_statement_params: dict = None,
):
    engine = get_db_engine(username, password, host, db_name)
    connection = engine.raw_connection()

    if where_statement_file is not None:
        if where_statement_params is None:
            where_statement_params = dict()
        where_statement = read_sql(
            sql_file=where_statement_file, **where_statement_params
        )
    else:
        where_statement = ""

    sql = get_row_count_sql(
        table_name=table_name,
        where_statement=where_statement,
    )

    LOGGER.info(f"The below sql statement will be executed: \n {sql}")
    cursor = connection.cursor()
    cursor.execute(sql)
    row_count = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    LOGGER.info("The sql statement is executed successfully\n")
    return row_count
