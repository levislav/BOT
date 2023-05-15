import sqlite3 as sqlite
import settings

structure = ['id', 'timer', 'department', 'progress']


def connect_db():
    global connect, cursor
    connect = sqlite.connect(settings.database)
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               id INT PRIMARY KEY,
               timer TEXT,
               department TEXT,
               progress INT
               )
       """)

    connect.commit()


async def start_db(users_list) -> None:
    global connect, cursor

    cursor.execute("INSERT OR REPLACE INTO users VALUES(?,?,?,?);", users_list)
    connect.commit()


async def get_db(obj: str, telegram_info: str) -> str:
    global connect, cursor
    cursor.execute(f"SELECT * FROM users")
    all_result = cursor.fetchall()
    for result in all_result:
        if result[0] == telegram_info:
            return result[structure.index(obj)]


async def update_db(obj1: str, obj2: str, telegram_info: str) -> None:
    global connect, cursor
    print(f"UPDATE users SET {obj1} = \"{obj2}\" WHERE id = \"{telegram_info}\"")
    cursor.execute("UPDATE users SET \"{obj1}\" = \"{obj2}\" WHERE id = \"{telegram_info}\";".format(obj1=obj1,
                                                                                                                     obj2=obj2,
                                                                                                                     telegram_info=telegram_info))
    connect.commit()

connect_db()
