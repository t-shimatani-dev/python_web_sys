import sqlite3
import unittest

from database.database_manager import DatabaseManager


class _FakeEngineDirectConnection:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def raw_connection(self):
        return self._conn


class _ConnectionWrapper:
    def __init__(self, conn: sqlite3.Connection):
        self.dbapi_connection = conn

    def cursor(self):
        return self.dbapi_connection.cursor()

    def commit(self):
        return self.dbapi_connection.commit()

    def close(self):
        return self.dbapi_connection.close()


class _FakeEngineWrappedConnection:
    def __init__(self, wrapper: _ConnectionWrapper):
        self._wrapper = wrapper

    def raw_connection(self):
        return self._wrapper


class TestDatabaseConnectionCompatibility(unittest.TestCase):
    def _build_manager_with_engine(self, engine) -> DatabaseManager:
        manager = DatabaseManager(":memory:")
        manager._engine = engine
        manager._SessionFactory = object()
        return manager

    def test_get_connection_supports_direct_dbapi_connection(self):
        direct_conn = sqlite3.connect(":memory:")
        manager = self._build_manager_with_engine(_FakeEngineDirectConnection(direct_conn))

        conn = manager.get_connection()
        self.assertIs(conn, direct_conn)

        cursor = conn.cursor()
        cursor.execute("SELECT 1 AS value")
        row = cursor.fetchone()
        self.assertEqual(row["value"], 1)

        cursor.close()
        conn.close()

    def test_get_connection_supports_wrapped_dbapi_connection(self):
        base_conn = sqlite3.connect(":memory:")
        wrapped = _ConnectionWrapper(base_conn)
        manager = self._build_manager_with_engine(_FakeEngineWrappedConnection(wrapped))

        conn = manager.get_connection()
        self.assertIs(conn, wrapped)
        self.assertIs(base_conn.row_factory, sqlite3.Row)

        cursor = conn.cursor()
        cursor.execute("SELECT 1 AS value")
        row = cursor.fetchone()
        self.assertEqual(row["value"], 1)

        cursor.close()
        conn.close()


if __name__ == "__main__":
    unittest.main()
