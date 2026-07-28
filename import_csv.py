"""
CSVインポートスクリプト

使用方法:
    python3 import_csv.py <csvファイルパス>

例:
    python3 import_csv.py /home/agio0021/projects/python_web_sys/data/sample_employees.csv
"""
import os
import sys


def main():
    if len(sys.argv) != 2:
        print("使用方法: python3 import_csv.py <csvファイルパス>")
        print("例: python3 import_csv.py /path/to/employees.csv")
        sys.exit(1)

    csv_path = sys.argv[1]

    if not os.path.isfile(csv_path):
        print(f"エラー: ファイルが見つかりません: {csv_path}")
        sys.exit(1)

    from config import Config
    from database.database_manager import DatabaseManager
    from utils.csv_handler import CSVHandler
    from utils.validator import DataValidator

    db = DatabaseManager(Config.DATABASE_PATH)
    if not db.initialize_database():
        print("エラー: データベースの初期化に失敗しました")
        sys.exit(1)

    handler = CSVHandler(db, DataValidator())
    count, errors = handler.import_from_csv(csv_path)

    print(f"インポート成功: {count}件")
    if errors:
        print(f"エラー: {len(errors)}件")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
