import asyncio
import aiomysql
from aiomysql import Error
from contextlib import asynccontextmanager

HOST = '127.0.0.1'
PORT = 3306
USER = ''
PASSWORD = ''
DATABASE = 'mytest'


@asynccontextmanager
async def aio_mysql_conn(user: str = USER, password: str = PASSWORD,
                         host: str = HOST, database: str = DATABASE) -> "conn":
    """
    The function creates context manager out of aiomysql connector object, and allows to use inside 'with' pattern.
    Hereby we can be sure that connection will be closed despite of any errors and made changes will be rolled back.
    :param user: username in DB
    :param password: password in DB
    :param host: ip address of DB
    :param database: database name, we can use it instead of USE 'db_name;' sql command
    :return: - aiomysql connector object
    """
    _conn = await aiomysql.connect(user=user, password=password, host=host, db=database)
    try:
        yield _conn
    except (Exception, Error) as ex:
        # if error happened all made changes during the connection will be rolled back:
        await _conn.rollback()
        # this statement re-raise error to let it be handled in outer scope:
        raise
    else:
        # if everything is fine commit all changes to save them in db:
        await _conn.commit()
    finally:
        # close connection to db, do not wait for timeout release:
        _conn.close()


@asynccontextmanager
async def aio_mysql_curs(user: str = USER, password: str = PASSWORD,
                         host: str = HOST, database: str = DATABASE) -> "curs":
    """
    The function creates context manager out of aiomysql cursor object, and allows to use inside 'with' pattern.
    Pay attention that aiomysql connection manager is used inside the function and answers for all error handling,
    which can happen when
    :return: aiomysql connector object
    """
    async with aio_mysql_conn(user, password, host, database) as _conn:
        _curs = await _conn.cursor()
        try:
            yield _curs
        finally:
            await _curs.close()  # close cursor when everything is done


async def test_example():
    async with aio_mysql_curs() as cur:
        await cur.execute("select * from tasks")
        x = await cur.fetchall()
        for i in x:
            print(i)
        print("*" * 50)

        await cur.execute("update tasks set title='EggoAsync' where task_id in (24, 25);")

        await cur.execute("select * from tasks")
        x = await cur.fetchall()
        for i in x:
            print(i)
        print("*" * 50)


async def main():
    await test_example()


if __name__ == '__main__':
    asyncio.run(main())
