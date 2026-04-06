# routes/employee_routes.py
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
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
        # 例外発生時でも必ず接続をクローズするために、try-finally構文を使用してデータベース操作を行う
        try:
            cursor = conn.cursor()
            
            # 一覧表示に必要な列のみ取得し、employee_id順（昇順）でソート
            cursor.execute("""
                SELECT employee_id, name, name_kana, department, position, hire_date, email
                FROM employees
                ORDER BY employee_id
            """)
            
            employees = cursor.fetchall()
        finally:
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
        # 例外発生時でも必ず接続をクローズするために、try-finally構文を使用してデータベース操作を行う
        try:
            cursor = conn.cursor()
            
            # URLパラメータで受け取った employee_id で社員レコードを1件取得
            cursor.execute("""
                SELECT * FROM employees WHERE employee_id = ?
            """, (employee_id,))
            
            employee = cursor.fetchone()
        finally:
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

# ステップ８：社員新規登録ルートの実装
# 社員新規登録ルート
@employee_bp.route('/employee/new', methods=['GET', 'POST'])
def new_employee():
    """社員新規登録"""
    if request.method == 'GET':
        # GETリクエスト: 入力値なしの空フォームを表示
        return render_template('employees/new.html')
    
    # POST処理（フォーム送信）
    try:
        # 関数内インポートで循環インポートを回避しつつDBマネージャーとバリデーターをインスタンス化
        from database.database_manager import DatabaseManager
        # ここでバリデーターをインポート
        from utils.validator import DataValidator
        
        # バリデーターをインスタンス化
        validator = DataValidator()
        
        # フォームデータ取得（前後の空白を除去する）
        employee_id = request.form.get('employee_id', '').strip()
        name = request.form.get('name', '').strip()
        name_kana = request.form.get('name_kana', '').strip()
        department = request.form.get('department', '').strip()
        position = request.form.get('position', '').strip()
        hire_date = request.form.get('hire_date', '').strip()
        salary = request.form.get('salary', '').strip()
        email = request.form.get('email', '').strip()
        
        # バリデーション
        errors = []
        
        # 各フィールドのバリデーションを実行し、エラーメッセージをerrorsリストに追加
        valid, msg = validator.validate_employee_id(employee_id)
        if not valid:
            errors.append(msg)
        
        valid, msg = validator.validate_name(name)
        if not valid:
            errors.append(msg)
        
        valid, msg = validator.validate_email(email)
        if not valid:
            errors.append(msg)
        
        valid, msg = validator.validate_hire_date(hire_date)
        if not valid:
            errors.append(msg)
        
        valid, msg = validator.validate_salary(salary)
        if not valid:
            errors.append(msg)
        
        # エラーがある場合: フラッシュメッセージで通知し、入力値を保持したまま再表示
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('employees/new.html', form_data=request.form)
        
        # DB挿入（バリデーション通過後に社員レコードをINSERT）
        from config import Config
        # データベースマネージャーをインスタンス化して接続を取得
        db_manager = DatabaseManager(Config.DATABASE_PATH)
        # データベース接続を取得してカーソルを作成
        conn = db_manager.get_connection()
 
        # 例外発生時でも必ず接続をクローズするために、try-finally構文を使用してデータベース操作を行う
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (
                    employee_id, name, name_kana, department, position,
                    hire_date, salary, email, phone, postal_code, address, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                employee_id, name, name_kana, department, position,
                hire_date, int(salary), email,
                request.form.get('phone', ''),
                request.form.get('postal_code', ''),
                request.form.get('address', ''),
                request.form.get('notes', '')
            ))
            conn.commit()
        finally:
            conn.close()  # 例外発生時でも必ず実行される
       
        logger.info(f"社員登録成功: {employee_id}")
        flash('社員情報を登録しました', 'success')
        return redirect(url_for('employee.index'))
        
    except Exception as e:
        logger.error(f"社員登録エラー: {e}")
        flash(f'登録に失敗しました: {str(e)}', 'danger')
        return render_template('employees/new.html', form_data=request.form)

@employee_bp.route('/employee/<employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """社員情報更新"""
    # 関数冒頭でGET/POST共通のDBマネージャーをインスタンス化
    from database.database_manager import DatabaseManager
    from config import Config
    db_manager = DatabaseManager(Config.DATABASE_PATH)
    
    if request.method == 'GET':
        # 既存データ取得（編集フォームに表示する現在の社員情報を取得）
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
            employee = cursor.fetchone()
        finally:
            conn.close()  # 例外発生時でも必ず実行される
        
        # 指定IDの社員が存在しない場合は404エラー
        if employee is None:
            abort(404)
        
        return render_template('employees/edit.html', employee=employee)
    
    # POST処理（フォーム送信による更新）
    try:
        from utils.validator import DataValidator
        # バリデーターをインスタンス化
        validator = DataValidator()
        
        # フォームデータ取得とバリデーション（D-06と同様）
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        salary = request.form.get('salary', '').strip()
        
        errors = []
        # バリデーション処理（省略）
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('employee.edit_employee', employee_id=employee_id))
        
        # DB更新
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employees SET
                    name = ?, name_kana = ?, department = ?, position = ?,
                    hire_date = ?, salary = ?, email = ?, phone = ?,
                    postal_code = ?, address = ?, notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE employee_id = ?
            """, (
                name, request.form['name_kana'], request.form['department'], request.form['position'],
                request.form['hire_date'], int(salary), email, request.form.get('phone', ''),
                request.form.get('postal_code', ''), request.form.get('address', ''),
                request.form.get('notes', ''), employee_id
            ))
            conn.commit()
        finally:
            conn.close()  # 例外発生時でも必ず実行される
        
        logger.info(f"社員情報更新: {employee_id}")
        flash('社員情報を更新しました', 'success')
        return redirect(url_for('employee.detail', employee_id=employee_id))
        
    except Exception as e:
        logger.error(f"社員更新エラー: {e}")
        flash(f'更新に失敗しました: {str(e)}', 'danger')
        return redirect(url_for('employee.edit_employee', employee_id=employee_id))

@employee_bp.route('/employee/<employee_id>/delete', methods=['GET', 'POST'])
def delete_employee(employee_id):
    """社員情報削除"""
    from database.database_manager import DatabaseManager
    from config import Config
    db_manager = DatabaseManager(Config.DATABASE_PATH)
    
    # 社員情報取得とDB操作をtry/finallyで囲み、例外発生時も必ずconn.close()が実行されるようにする
    conn = db_manager.get_connection()
    # 例外発生時でも必ず接続をクローズするために、try-finally構文を使用してデータベース操作を行う
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
        employee = cursor.fetchone()
        
        # 指定IDの社員が存在しない場合は404エラー
        if employee is None:
            abort(404)
        
        if request.method == 'GET':
            # GETリクエスト: 削除確認画面を表示（社員情報をテンプレートに渡す）
            return render_template('employees/delete.html', employee=employee)
        
        # POST処理: 削除確認後の実際のDELETE実行
        try:
            # DELETEクエリをパラメータ化クエリで実行し、コミットで確定する
            cursor.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
            conn.commit()
            
            logger.info(f"社員情報削除: {employee_id}")
            flash(f'社員情報を削除しました: {employee_id}', 'success')
            return redirect(url_for('employee.index'))
            
        except Exception as e:
            logger.error(f"社員削除エラー: {e}")
            flash(f'削除に失敗しました: {str(e)}', 'danger')
            return redirect(url_for('employee.detail', employee_id=employee_id))
    finally:
        conn.close()  # GET/POST/例外発生のいずれでも必ず実行される

@employee_bp.route('/search')
def search():
    """社員検索"""
    try:
        # 関数内インポートで循環インポートを回避しつつDBマネージャーをインスタンス化
        from database.database_manager import DatabaseManager
        from config import Config
        db_manager = DatabaseManager(Config.DATABASE_PATH)
        
        # クエリパラメータ取得（未入力の場合は空文字として扱う）
        query_name = request.args.get('name', '').strip()
        query_department = request.args.get('department', '').strip()
        query_position = request.args.get('position', '').strip()
        
        # SQL構築（動的WHERE句）: 入力された条件のみWHERE句に追加する
        where_clauses = []
        params = []
        
        if query_name:
            where_clauses.append("name LIKE ?")
            params.append(f"%{query_name}%")
        
        if query_department:
            where_clauses.append("department LIKE ?")
            params.append(f"%{query_department}%")
        
        if query_position:
            where_clauses.append("position LIKE ?")
            params.append(f"%{query_position}%")
        
        # WHERE句結合: 条件があれば AND で連結、なければ全件取得（1=1）
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        sql = f"""
            SELECT employee_id, name, name_kana, department, position, hire_date, email
            FROM employees
            WHERE {where_sql}
            ORDER BY employee_id
        """
        
        conn = db_manager.get_connection()
        # 例外発生時でも必ず接続をクローズするために、try-finally構文を使用してデータベース操作を行う
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            employees = cursor.fetchall()
        finally:
            conn.close()  # 例外発生時でも必ず実行される
        
        logger.info(f"検索実行: {len(employees)}件")
        return render_template('employees/search.html',
                             employees=employees,
                             query_name=query_name,
                             query_department=query_department,
                             query_position=query_position)
        
    except Exception as e:
        logger.error(f"検索エラー: {e}")
        flash(f'検索に失敗しました: {str(e)}', 'danger')
        return render_template('employees/search.html', employees=[])