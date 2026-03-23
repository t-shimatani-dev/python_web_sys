# database/database_manager.py
import sqlite3
import logging
from pathlib import Path
from config import Config

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path=None):
        """
        コンストラクタ
        
        Args:
            db_path (str, optional): データベースファイルパス
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self.logger = logging.getLogger(__name__)
    
    def initialize_database(self):
        """
        データベースとテーブルを初期化
        
        Returns:
            bool: 成功時True、失敗時False
        """
        try:
            # データベースディレクトリ作成
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
                "CREATE INDEX IF NOT EXISTS idx_employee_name ON employees(name)",
                "CREATE INDEX IF NOT EXISTS idx_employee_department ON employees(department)",
                "CREATE INDEX IF NOT EXISTS idx_employee_hire_date ON employees(hire_date)"
            ]
            
            for index_sql in index_sqls:
                cursor.execute(index_sql)
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Database initialized successfully: {self.db_path}")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization failed: {e}")
            return False
    
    def get_connection(self):
        """
        データベース接続を取得
        
        Returns:
            sqlite3.Connection: データベース接続オブジェクト
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # 辞書形式で取得
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            raise

if __name__ == "__main__":
    # テスト実行
    from utils.logger import setup_logger
    setup_logger()
    
    db_manager = DatabaseManager()
    success = db_manager.initialize_database()
    
    if success:
        print("✓ データベース初期化成功")
        
        # テーブル確認
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"テーブル一覧: {[t[0] for t in tables]}")
        conn.close()
    else:
        print("✗ データベース初期化失敗")