from contextlib import contextmanager
import mysql.connector
from mysql.connector.errors import Error

USER = ''
PASSWORD = ''
HOST = '127.0.0.1'
DATABASE = 'mytest'


@contextmanager
def mysql_connection(user: str = USER, password: str = PASSWORD, host: str = HOST, database: str = DATABASE) -> "conn":
    """
    The function creates context manager out of mysql connector object, and allows to use inside 'with' pattern.
    Hereby we can be sure that connection will be closed despite of any errors and made changes will be rolled back.
    :param user: username in DB
    :param password: password in DB
    :param host: ip address of DB
    :param database: database name, we can use it instead of USE 'db_name;' sql command
    :return: - mysql connector object
    """
    _conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    try:
        yield _conn
    except (Exception, Error) as ex:
        # if error happened all made changes during the connection will be rolled back:
        _conn.rollback()
        # this statement re-raise error to let it be handled in outer scope:
        raise
    else:
        # if everything is fine commit all changes to save them in db:
        _conn.commit()
    finally:
        # close connection to db, do not wait for timeout release:
        _conn.close()


@contextmanager
def mysql_curs() -> "curs":
    """
    The function creates context manager out of mysql cursor object, and allows to use inside 'with' pattern.
    Pay attention that mysql connection manager is used inside the function and answers for all error handling,
    which can happen when
    :return: mysql connector object
    """
    with mysql_connection(USER, PASSWORD, HOST, DATABASE) as _conn:
        _curs = _conn.cursor()
        try:
            yield _curs
        finally:
            _curs.close()  # close cursor when everything is done


if __name__ == '__main__':
    with mysql_curs() as curs:
        curs.execute("INSERT INTO tasks (title) VALUE ('Mark');")
        #raise Error("Hey!")
        curs.execute("SELECT * FROM tasks;")
        x = curs.fetchall()
        print(x)
