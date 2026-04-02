# database/database_manager.py
import sqlite3
import logging
from pathlib import Path


class DatabaseManager:
    """データベース管理クラス"""

    def __init__(self, db_path):
        """
        コンストラクタ

        Args:
            db_path (str): データベースファイルパス
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def initialize_database(self):
        """データベースとテーブルを初期化
        
        Returns:
            bool: 成功時にTrue、失敗時にFalse
        """
        
        if not Path(self.db_path).exists():
            self.logger.info(f"Database file {self.db_path} does not exist. Creating new database.")
        
        try:
            # データベースディレクトリが存在しない場合は作成
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)

            # データベース接続
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # テーブル作成SQL
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                name_kana TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                salary INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                postal_code TEXT,
                address TEXT,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """

            cursor.execute(create_table_sql)

            # インデックス作成
            index_sqls = [
                "CREATE INDEX IF NOT EXISTS idx_employees_name ON employees(name)",
                "CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department)",
                "CREATE INDEX IF NOT EXISTS idx_employees_hire_date ON employees(hire_date)"
            ]

            for index_sql in index_sqls:
                cursor.execute(index_sql)

            conn.commit()
            conn.close()

            self.logger.info(f"Database initialized successfully at {self.db_path}")
            return True
        
        except sqlite3.Error as e:
            self.logger.error(f"Error! Database initialized failed : {e}")
            return False

    def get_connection(self):
        """
        データベース接続を取得
        
        Returns:
            sqlite3.Connection: データベース接続オブジェクト
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # 結果を辞書形式で取得
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Error! Database connection failed : {e}")
            raise
    
    def save_employee(self, row_data: dict) -> None:
        """社員データをDBに保存する（既存の場合は更新）
        
        Args:
            row_data (dict): CSVの1行データ。キーはCSVヘッダー名（日本語）
        
        Raises:
            sqlite3.Error: データベース操作に失敗した場合
        """
        sql="""
        INSERT OR REPLACE INTO employees 
            (employee_id, name, name_kana, department, position,
             hire_date, salary, email, updated_at)
        VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        params = (
            row_data['社員ID'],
            row_data['氏名'],
            row_data['氏名カナ'],
            row_data['部署'],
            row_data['役職'],
            row_data['入社日'],
            int(row_data['給与']),
            row_data['メールアドレス'],
        )
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            self.logger.info(f"社員データを保存しました: {row_data['社員ID']}")
        except sqlite3.Error as e:
            conn.rollback()
            self.logger.error(f"社員データの保存に失敗しました: {e}")
            raise
        finally:
            conn.close()

# 動作確認用テストブロック
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    from config import Config

    db_manager = DatabaseManager(Config.DATABASE_PATH)
    success = db_manager.initialize_database()

    if success:
        print("✓ データベース初期化成功")
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"テーブル一覧: {[dict(t)['name'] for t in tables]}")
        conn.close()
    else:
        print("✗ データベース初期化失敗")
