# database/database_manager.py（SQLAlchemy版）
import logging
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from database.models import Base, Employee


class DatabaseManager:
    """データベース管理クラス（SQLAlchemy版）"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._engine = None
        self._SessionFactory = None

    def initialize_database(self) -> bool:
        """データベースとテーブルを初期化

        Returns:
            bool: 成功時にTrue、失敗時にFalse
        """
        try:
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)

            # エンジン作成（sqlite:///は相対パス、sqlite:////は絶対パス）
            self._engine = create_engine(f"sqlite:///{self.db_path}", echo=False)

            # モデル定義からテーブル・インデックスを自動生成（CREATE TABLE IF NOT EXISTS相当）
            Base.metadata.create_all(self._engine)

            self._SessionFactory = sessionmaker(bind=self._engine)

            self.logger.info(f"Database initialized successfully: {self.db_path}")
            return True

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            return False

    def _ensure_initialized(self) -> None:
        """内部利用: 未初期化なら初期化を試行する"""
        if self._SessionFactory is None or self._engine is None:
            initialized = self.initialize_database()
            if not initialized:
                raise RuntimeError("データベース初期化に失敗しました")

    def get_session(self) -> Session:
        """DBセッションを取得（with文で使用すること）

        Returns:
            Session: SQLAlchemyセッションオブジェクト

        Example:
            with db_manager.get_session() as session:
                employees = session.query(Employee).all()
        """
        self._ensure_initialized()
        return self._SessionFactory()

    def get_connection(self):
        """互換API: sqlite3ライクな接続を返す（既存routes向け）"""
        self._ensure_initialized()
        # SQLAlchemy経由でDB-API接続を取得すると cursor/commit/close が利用できる
        conn = self._engine.raw_connection()
        # テンプレート側の属性アクセス互換のため sqlite3.Row を返す。
        conn.dbapi_connection.row_factory = sqlite3.Row
        return conn

    def employee_exists(self, employee_id: str, email: str) -> bool:
        """社員IDまたはメールアドレスが既存レコードと重複するかを確認する。"""
        self._ensure_initialized()

        with self.get_session() as session:
            exists = (
                session.query(Employee)
                .filter((Employee.employee_id == employee_id) | (Employee.email == email))
                .first()
            )
            return exists is not None

    def save_employee(self, row_data: dict) -> None:
        """CSVの1行データをemployeesテーブルに保存する"""
        self._ensure_initialized()

        employee = Employee(
            employee_id=row_data.get("社員ID", ""),
            name=row_data.get("氏名", ""),
            name_kana=row_data.get("氏名カナ", ""),
            department=row_data.get("部署", ""),
            position=row_data.get("役職", ""),
            hire_date=row_data.get("入社日", ""),
            salary=int(row_data.get("給与", 0)),
            email=row_data.get("メールアドレス", ""),
            phone=row_data.get("電話番号", ""),
            postal_code=row_data.get("郵便番号", ""),
            address=row_data.get("住所", ""),
            notes=row_data.get("備考", ""),
        )

        try:
            with self.get_session() as session:
                session.add(employee)
                session.commit()
        except IntegrityError as e:
            raise ValueError("社員IDまたはメールアドレスが重複しています") from e
