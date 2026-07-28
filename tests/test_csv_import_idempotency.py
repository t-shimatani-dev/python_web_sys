import csv
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

    def test_intra_csv_duplicate_rows_are_skipped(self):
        """
        1回のインポート内で社員ID/メールが重複するCSVを使い、
        成功1件・エラー0・DB件数1件になることを確認する。
        """
        base_csv_path = Path(__file__).resolve().parents[1] / "data" / "sample_employees.csv"

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = str(Path(tmp_dir) / "employees_intra_dup.db")
            db = DatabaseManager(db_path)
            self.assertTrue(db.initialize_database())

            duplicated_csv_path = Path(tmp_dir) / "employees_intra_dup.csv"
            with base_csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)

            self.assertGreaterEqual(len(rows), 2, "sample_employees.csv はヘッダー+1行以上必要です")

            header = rows[0]
            first_row = rows[1]

            with duplicated_csv_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(first_row)
                writer.writerow(first_row)

            handler = CSVHandler(db, DataValidator())
            count, errors = handler.import_from_csv(str(duplicated_csv_path))

            self.assertEqual(count, 1)
            self.assertEqual(errors, [])

            with db.get_session() as session:
                total = session.query(Employee).count()
            self.assertEqual(total, 1)

    def test_partial_duplicate_and_new_rows_are_handled(self):
        """
        1回目で5件投入後、2回目に既存3件+新規2件を投入し、
        成功2件・エラー0・DB件数7件になることを確認する。
        """
        base_csv_path = Path(__file__).resolve().parents[1] / "data" / "sample_employees.csv"

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = str(Path(tmp_dir) / "employees_partial_dup.db")
            db = DatabaseManager(db_path)
            self.assertTrue(db.initialize_database())

            handler = CSVHandler(db, DataValidator())

            first_count, first_errors = handler.import_from_csv(str(base_csv_path))
            self.assertEqual(first_errors, [])
            self.assertEqual(first_count, 5)

            partial_csv_path = Path(tmp_dir) / "employees_partial_dup.csv"

            with base_csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)

            self.assertGreaterEqual(len(rows), 4, "sample_employees.csv はヘッダー+3行以上必要です")

            header = rows[0]
            existing_rows = rows[1:4]

            header_to_index = {name: i for i, name in enumerate(header)}
            employee_id_index = header_to_index.get("社員ID")
            email_index = header_to_index.get("メールアドレス")

            self.assertIsNotNone(employee_id_index, "社員ID カラムが必要です")
            self.assertIsNotNone(email_index, "メールアドレス カラムが必要です")

            base_row = list(rows[1])

            new_row_1 = base_row.copy()
            new_row_1[employee_id_index] = "A9999"
            new_row_1[email_index] = "new9999@example.com"

            new_row_2 = base_row.copy()
            new_row_2[employee_id_index] = "A9998"
            new_row_2[email_index] = "new10000@example.com"

            with partial_csv_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(existing_rows)
                writer.writerow(new_row_1)
                writer.writerow(new_row_2)

            second_count, second_errors = handler.import_from_csv(str(partial_csv_path))
            self.assertEqual(second_errors, [])
            self.assertEqual(second_count, 2)

            with db.get_session() as session:
                total = session.query(Employee).count()
            self.assertEqual(total, 7)


if __name__ == "__main__":
    unittest.main()
