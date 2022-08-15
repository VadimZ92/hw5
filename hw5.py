import psycopg2


def DROP_TABLE(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone;
            DROP TABLE client;
            """)
        conn.commit()
    print("Таблицы удалены")


def CREATE_TABLE():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) UNIQUE,
                surname VARCHAR(40) UNIQUE,
                e_mail VARCHAR(40) UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                number INTEGER UNIQUE,
                client_id INTEGER NOT NULL REFERENCES client(id)
            );
            """)
        conn.commit()
    print("Таблицы созданы")


def INSERT_C(conn, name1, surname1, e_mail1):
    with conn.cursor() as cur:
        cur.execute(f"""INSERT INTO client(name, surname, e_mail) 
                        VALUES('{name1}', '{surname1}', '{e_mail1}') RETURNING id;""")
        conn.commit()
        print(cur.fetchone())


def INSERT_P(conn, number1, client_id1):
    with conn.cursor() as cur:
        cur.execute(f"""INSERT INTO phone(number, client_id) VALUES('{number1}', '{client_id1}') RETURNING id;""")
        conn.commit()
        print(cur.fetchone())


def UPDATE_C(conn, client_id, name1, surname1, e_mail1):
    with conn.cursor() as cur:
        cur.execute("""UPDATE client SET name=%s, surname=%s, e_mail=%s WHERE id=%s;""",
                    (name1, surname1, e_mail1, client_id))
        cur.execute("""
                SELECT * FROM client;
                """)
        conn.commit()
        print(cur.fetchall())


def DELETE_P(conn, number):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phone WHERE number=%s;
                """, (number,))
        cur.execute("""
                SELECT * FROM phone;
                """)
        conn.commit()
        print(cur.fetchall())


def DELETE_С(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                       DELETE FROM phone WHERE client_id=%s;
                       """, (client_id,))
        cur.execute("""
                       SELECT * FROM phone;
                       """)
        cur.execute("""
                DELETE FROM client WHERE id=%s;
                """, (client_id,))
        cur.execute("""
                SELECT * FROM client;
                """)
        conn.commit()
        print(cur.fetchall())


def SEARCH(conn, data1, data3):
    with conn.cursor() as cur:
        cur.execute(f"""
                SELECT name, surname, e_mail, number FROM client
                JOIN phone ON phone.client_id = client.id 
                WHERE {data1}={data3}            
                """)
        print('Клиент', cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="*****", user="******", password="********") as conn:
        while True:
            command = input("Введите команду:\n"
                            "(ct - Создать таблицы)\n"
                            "(ac - Добавить клиента)\n"
                            "(ap - Добавить телефон)\n"
                            "(up - Изменить данные клиента)\n"
                            "(dp - Удалить номер телефона)\n"
                            "(dc - Удалить запись клиента)\n"
                            "(s - Поиск клиента)\n"
                            "(d - Удаление таблиц)\n"
                            "(q - Выход):\n")
            if command == "ct":
                CREATE_TABLE()
            elif command == "ac":
                INSERT_C(conn, name1=input("Введите имя:\n"),
                         surname1=input("Введите фамилию:\n"),
                         e_mail1=input("Введите e-mail:\n"))
            elif command == "ap":
                INSERT_P(conn, number1=input("Введите номер телефона:\n"),
                         client_id1=input("Введите id клиента:\n"))
            elif command == "up":
                UPDATE_C(conn, client_id=input("Введите id клиента:\n"),
                         name1=input("Введите новое имя:\n"),
                         surname1=input("Введите новую фамилию:\n"),
                         e_mail1=input("Введите новый e-mail:\n"))
            elif command == "dp":
                DELETE_P(conn, number=input("Введите номер, который нужно удалить:\n"))
            elif command == "dc":
                DELETE_С(conn, client_id=input("Введите id клиента, которого нужно удалить:\n"))
            elif command == "s":
                data = input("имя, фамилия, e-mail или номер?:\n")
                if data == "имя":        ## data1 и data3 нужны для исключения ошибки, чтобы опрделить
                    data1 = 'name'       ## будем вводить номер или имя/фамилию/емейл. Так как для ввода
                elif data == "фамилия":  ## имени/фамилии/емейла нужна строка, а для ввода номера число.
                    data1 = 'surname'    ## Поэтому, сначала понимаем какой параметр ищем, а потом предоставляем
                elif data == "e-mail":   ## данные с "кавычками" или без. (строку или число).
                    data1 = 'e_mail'
                elif data == "номер":
                    data1 = 'number'
                data2 = input("Введите запрашиваемые данные:\n")
                if data1 == 'name' or 'surname' or 'e_mail':
                    data3 = f"'{data2}'"
                elif data1 == 'number':
                    data3 = data2
                SEARCH(conn, data1, data3)
            elif command == "d":
                DROP_TABLE(conn)
            elif command == "q":
                print("Выход")
                break

conn.close()
