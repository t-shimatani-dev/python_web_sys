# app.py
try:
    from flask import Flask
except ModuleNotFoundError as exc:
    if exc.name == "flask":
        raise ModuleNotFoundError(
            "No module named 'flask'. This project uses uv-managed dependencies. "
            "Run 'uv sync' and then start the app with 'uv run python app.py' "
            "(or activate the correct virtual environment)."
        ) from exc
    raise

from config import Config
from utils.logger import setup_logger

# アプリケーションファクトリーパターンを採用する事で下記のメリットがある
# - アプリの設定や拡張機能の初期化を一元管理できる
# - テストの際に異なる設定でアプリを簡単に作成できる
# - 循環インポートを回避できる

def create_app():
    """Flaskアプリケーションファクトリー関数"""
    # Flaskアプリのインスタンスを作成（__name__でテンプレート等のパスを自動解決）
    app = Flask(__name__)
    # アプリの設定をルートディレクトリ直下のconfig.pyから読み込む
    app.config.from_object(Config)
    # アプリ用のロギング設定を初期化（utils/logger.pyのsetup_logger関数）
    setup_logger()
    # 従業員関連のルート（URLエンドポイント）をまとめたBlueprintを読み込み、アプリに登録する。
    # 下記のインポートは関数内で行うことで、循環インポートを回避する。
    from routes.employee_routes import employee_bp

    app.register_blueprint(employee_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
