
import psycopg2

class DBManager:
    
    def __init__(self, db_name : str, user_name : str, passw : str) -> None:
        self._db = db_name
        try:
            self._conn = psycopg2.connect(database = db_name, user = user_name, password = passw)
            #self._conn.autocommit = False
            print(self.SelfStatus())
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY NOT NULL,
                    first_name VARCHAR(120),
                    last_name VARCHAR(120),
                    e_mail VARCHAR(120) );
                """)
                self._conn.commit()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clients_phones_dep(
                    client_id INTEGER NOT NULL REFERENCES clients(client_id),
                    client_phone BIGINT NOT NULL,
                    CONSTRAINT idp_pk PRIMARY KEY (client_id, client_phone) );
                """)
                self._conn.commit()
        except psycopg2.OperationalError as e:
            self._conn = None
            print('Unable to connect: %s!' % e)
    
    def SelfStatus(self) -> tuple:
        return self._conn.status, self._conn

    def AddClient(self, first_name : str, last_name : str, email : str, client_id : int = None) -> int:
        ret_val = 0
        try:
            with self._conn.cursor() as cursor:
                if client_id is None:
                    cursor.execute("""
                        INSERT INTO clients(first_name, last_name, e_mail)
                        VALUES(%s, %s, %s)
                        RETURNING client_id;
                    """, (first_name, last_name, email))
                else:
                    print("client id " + str(client_id))
                    cursor.execute("""
                        INSERT INTO clients(client_id, first_name, last_name, e_mail)
                        VALUES(%s, %s, %s, %s)
                        RETURNING client_id;
                    """, (client_id, first_name, last_name, email))
                ret = cursor.fetchall()
                ret_val = ret[0][0]
        except Exception as e:
            print(e)
        self._conn.commit()
        return ret_val

    def AddClientPhone(self, client_id : int, client_phone : int) -> int:
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO clients_phones_dep(client_id, client_phone)
                    VALUES(%s, %s)
                    RETURNING client_id;
                """, (str(client_id), str(client_phone),))
                ret = cursor.fetchall()
                self._conn.commit()
                return ret[0][0]
        except Exception as e:
            print(e)
            self._conn.commit()
            return 0
    
    def ChangeClientData(self, client_id : int, first_name : str, last_name : str, email : str) -> int:
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE clients
                    SET first_name=%s,
                    last_name=%s,
                    e_mail=%s
                    WHERE client_id=%s
                    RETURNING client_id;
                """, (first_name, last_name, email, client_id))
                ret = cursor.fetchall()
                self._conn.commit()
                return ret[0][0]
        except Exception as e:
            print(e)
            self._conn.commit()
            return 0
    
    def RemoveClientPhone(self, client_id : int, phone : int) -> int:
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM clients_phones_dep
                    WHERE client_id=%s AND client_phone=%s
                    RETURNING client_id;
                """, (client_id, phone))
                ret = cursor.fetchall()
                self._conn.commit()
                return ret[0][0]
        except Exception as e:
            print(e)
            self._conn.commit()
            return 0

    def RemoveClient(self, client_id : int) -> int:
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM clients_phones_dep
                    WHERE client_id=%s;
                """, (client_id,))
                self._conn.commit()
                cursor.execute("""
                    DELETE FROM clients
                    WHERE client_id=%s;
                """, (client_id,))
                self._conn.commit()
                return 1
        except Exception as e:
            print(e)
            self._conn.commit()
            return 0

    def FindClient(self, first_name : str = '%', last_name : str = '%', email : str = '%') -> list:
        ret_val = []
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    SELECT client_id, first_name, last_name, e_mail FROM clients
                    WHERE first_name LIKE (%s) AND last_name LIKE(%s) AND e_mail LIKE(%s);
                """, (first_name, last_name, email))
                ret_val = cursor.fetchall()
        except Exception as e:
            print(e)
        self._conn.commit()
        return ret_val

    def CloseDB(self):
        self._conn.close()
        print(self.SelfStatus())

    # game over



