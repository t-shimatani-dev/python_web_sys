import tempfile
import unittest
from pathlib import Path

from utils.csv_handler import CSVHandler
from utils.exceptions import DuplicateEmployeeException


class _NoopValidator:
    def validate_employee_data(self, row_data):
        return []


class _DuplicateOnSaveDBManager:
    def __init__(self):
        self.calls = 0

    def employee_exists(self, employee_id, email):
        return False

    def save_employee(self, row_data):
        self.calls += 1
        raise DuplicateEmployeeException("duplicate message can change")


class TestCSVHandlerDuplicateException(unittest.TestCase):
    def test_duplicate_exception_is_skipped_without_error_message_match(self):
        header = "社員ID,氏名,氏名カナ,部署,役職,入社日,給与,メールアドレス\n"
        row = "E001,山田太郎,ヤマダタロウ,営業部,主任,2020-04-01,5000000,yamada@example.com\n"

        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "one_row.csv"
            csv_path.write_text(header + row, encoding="utf-8")

            db_manager = _DuplicateOnSaveDBManager()
            handler = CSVHandler(db_manager, _NoopValidator())

            success_count, error_messages = handler.import_from_csv(str(csv_path))

        self.assertEqual(db_manager.calls, 1)
        self.assertEqual(success_count, 0)
        self.assertEqual(error_messages, [])


if __name__ == "__main__":
    unittest.main()
