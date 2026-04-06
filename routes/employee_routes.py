# routes/employee_routes.py
from flask import Blueprint, render_template, abort
from werkzeug.exceptions import HTTPException
import logging

# employee_bpの名前でBlueprintを作成
employee_bp = Blueprint('employee', __name__)
# ロガーの設定
logger = logging.getLogger(__name__)

@employee_bp.route('/')
def index():
    """社員一覧表示"""
    try:
        # 関数内インポートで循環インポートを回避しつつDBマネージャーをインスタンス化
        from database.database_manager import DatabaseManager
        from config import Config
        # データベースマネージャーをインスタンス化して接続を取得
        db_manager = DatabaseManager(Config.DATABASE_PATH)
        # データベース接続を取得してカーソルを作成
        conn = db_manager.get_connection()
        # カーソルを作成してSQLクエリを実行
        cursor = conn.cursor()

        # 一覧表示に必要な列のみ取得し、employee_id順（昇順）でソート
        cursor.execute("""
            SELECT employee_id, name, name_kana, department, position, hire_date, email
            FROM employees
            ORDER BY employee_id
        """)

        # クエリ結果を全件取得してリストに格納
        employees = cursor.fetchall()
        # データベース接続をクローズ
        conn.close()

        logger.info(f"社員一覧表示:{len(employees)}件")
        return render_template('employees/list.html', employees=employees)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"社員一覧の取得に失敗: {e}")
        abort(500, description="社員一覧の取得に失敗しました。")

@employee_bp.route('/employee/<employee_id>')
def detail(employee_id):
    """社員詳細表示"""
    try:
        # 関数内インポートで循環インポートを回避しつつDBマネージャーをインスタンス化
        from database.database_manager import DatabaseManager
        from config import Config
        # データベースマネージャーをインスタンス化して接続を取得
        db_manager = DatabaseManager(Config.DATABASE_PATH)
        # データベース接続を取得してカーソルを作成
        conn = db_manager.get_connection()
        # カーソルを作成してSQLクエリを実行
        cursor = conn.cursor()

        # URLパラメータで受け取った employee_id で社員レコードを1件取得
        cursor.execute("""
            SELECT * FROM employees WHERE employee_id = ?
        """, (employee_id,))

        # クエリ結果を1件取得して変数に格納
        employee = cursor.fetchone()
        # データベース接続をクローズ
        conn.close()

        # 指定IDの社員が存在しない場合は404エラーを返す
        if employee is None:
            logger.warning(f"社員ID {employee_id} が見つかりませんでした。")
            abort(404, description="社員が見つかりませんでした。")

        logger.info(f"社員詳細表示：社員ID {employee_id}")
        return render_template('employees/detail.html', employee=employee)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"社員詳細の取得に失敗: {e}")
        abort(500, description="社員詳細の取得に失敗しました。")
