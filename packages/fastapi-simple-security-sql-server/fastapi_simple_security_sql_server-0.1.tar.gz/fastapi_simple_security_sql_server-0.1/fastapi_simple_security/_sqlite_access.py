import pyodbc
import os
import uuid
import threading
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import pyodbc


class SqlServerAccess:
    def __init__(self):
        self.db_location = os.environ["Db"]
        
        try:
            self.expiration_limit = int(os.environ["FAST_API_SIMPLE_SECURITY_AUTOMATIC_EXPIRATION"])
        except KeyError:
            self.expiration_limit = 15

        self.init_db()

    def init_db(self):
        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()
            try:
                c.execute(
                    """
                    CREATE TABLE fastapi_simple_security (
                            id int IDENTITY(1,1) PRIMARY KEY,
                            api_key CHAR(100) UNIQUE,
                            is_active INTEGER,
                            never_expire INTEGER,
                            expiration_date CHAR(50),
                            latest_query_date CHAR(50),
                            total_queries INTEGER,
                            username CHAR(200) UNIQUE
                            )
                    """
                )
                connection.commit()
            except:
                print("Table already exists")

    def create_key(self, never_expire, username) -> str:
        api_key = str(uuid.uuid4())

        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()
            c.execute(
                """
                INSERT INTO fastapi_simple_security 
                (api_key, is_active, never_expire, expiration_date, latest_query_date, total_queries,username) 
                VALUES(?, ?, ?, ?, ?, ?,?)
            """,
                (
                    api_key,
                    1,
                    1 if never_expire else 0,
                    (datetime.utcnow() + timedelta(days=self.expiration_limit)).isoformat(timespec="seconds"),
                    None,
                    0,
                    username
                ),
            )
            connection.commit()

        return api_key

    def renew_key(self, api_key: str, new_expiration_date: str) -> Optional[str]:
        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()

            # We run the query like check_key but will use the response differently
            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM fastapi_simple_security 
            WHERE api_key = ?""",
                (api_key,),
            )

            response = c.fetchone()

            # API key not found
            if not response:
                return "API key not found"

            response_lines = []

            # Previously revoked key. Issue a text warning and reactivate it.
            if response[0] == 0:
                response_lines.append("This API key was revoked and has been reactivated.")
            # Expired key. Issue a text warning and reactivate it.
            if (not response[3]) and (datetime.fromisoformat(response[2]) < datetime.utcnow()):
                response_lines.append("This API key was expired and is now renewed.")

            if not new_expiration_date:
                parsed_expiration_date = (datetime.utcnow() + timedelta(days=self.expiration_limit)).isoformat(
                    timespec="seconds"
                )
            else:
                try:
                    # We parse and re-write to the right timespec
                    parsed_expiration_date = datetime.fromisoformat(new_expiration_date).isoformat(timespec="seconds")
                except ValueError:
                    return "The expiration date could not be parsed. Please use ISO 8601."

            c.execute(
                """
            UPDATE fastapi_simple_security
            SET expiration_date = ?, is_active = 1
            WHERE api_key = ?
            """,
                (parsed_expiration_date, api_key,),
            )

            connection.commit()

            response_lines.append(f"The new expiration date for the API key is {parsed_expiration_date}")

            return " ".join(response_lines)

    def revoke_key(self, api_key: str):
        """
        Revokes an API key

        Args:
            api_key: the API key to revoke
        """
        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()

            c.execute(
                """
            UPDATE fastapi_simple_security
            SET is_active = 0
            WHERE api_key = ?
            """,
                (api_key,),
            )

            connection.commit()

    def check_key(self, api_key: str) -> bool:
        """
        Checks if an API key is valid

        Args:
             api_key: the API key to validate
        """

        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()

            c.execute(
                """
            SELECT is_active, total_queries, expiration_date, never_expire
            FROM fastapi_simple_security 
            WHERE api_key = ?""",
                (api_key,),
            )

            response = c.fetchone()

            if (
                # Cannot fetch a row
                not response
                # Inactive
                or response[0] != 1
                # Expired key
                or ((not response[3]) and (datetime.fromisoformat(response[2]) < datetime.utcnow()))
            ):
                # The key is not valid
                return False
            else:
                # The key is valid

                # We run the logging in a separate thread as writing takes some time
                # NEVER EVER DO THIS PLEASE MAJOR THREAD UNSAFETY
                # Besides we don't want this given our use case.
                # threading.Thread(target=self._update_usage, args=(api_key, response[1],)).start()

                # We return directly
                return True

    def _update_usage(self, api_key: str, usage_count: int):
        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()

            # If we get there, this means it’s an active API key that’s in the database. We update the table.
            c.execute(
                """
            UPDATE fastapi_simple_security
            SET total_queries = total_queries + ?, latest_query_date = ?
            WHERE api_key = ?
            """,
                (usage_count, datetime.utcnow().isoformat(timespec="seconds"), api_key),
            )

            connection.commit()

    def get_usage_stats(self) -> List[Tuple[str, int, int, str, str, int,str]]:
        """
        Returns usage stats for all API keys

        Returns:
            a list of tuples with values being api_key, is_active, expiration_date, latest_query_date, total_queries and username
        """
        with pyodbc.connect(self.db_location) as connection:
            c = connection.cursor()

            # TODO Add filtering somehow
            c.execute(
                """
            SELECT api_key, is_active, never_expire, expiration_date, latest_query_date, total_queries, username
            FROM fastapi_simple_security
            ORDER BY latest_query_date DESC
            """,
            )

            response = c.fetchall()

        return response


sqlite_access = SqlServerAccess()
