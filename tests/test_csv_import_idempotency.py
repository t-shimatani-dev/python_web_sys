import tempfile
import unittest
from pathlib import Path

from database.database_manager import DatabaseManager
from database.models import Employee
from utils.csv_handler import CSVHandler
from utils.validator import DataValidator


class TestCSVImportIdempotency(unittest.TestCase):
    def test_reimport_same_csv_does_not_raise_duplicate_errors(self):
        csv_path = Path(__file__).resolve().parents[1] / "data" / "sample_employees.csv"

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = str(Path(tmp_dir) / "employees.db")
            db = DatabaseManager(db_path)
            self.assertTrue(db.initialize_database())

            handler = CSVHandler(db, DataValidator())

            first_count, first_errors = handler.import_from_csv(str(csv_path))
            self.assertEqual(first_count, 5)
            self.assertEqual(first_errors, [])

            second_count, second_errors = handler.import_from_csv(str(csv_path))
            self.assertEqual(second_count, 0)
            self.assertEqual(second_errors, [])

            with db.get_session() as session:
                total = session.query(Employee).count()
            self.assertEqual(total, 5)


if __name__ == "__main__":
    unittest.main()
