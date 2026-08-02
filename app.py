# app.py
import os

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


def _env_flag(name: str, default: bool = False) -> bool:
    """環境変数の真偽値を解釈する。"""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    app = create_app()
    app_env = os.getenv("APP_ENV", os.getenv("FLASK_ENV", "development")).lower()
    debug_enabled = _env_flag("FLASK_DEBUG", default=app_env != "production")
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))

    # 本番環境ではデバッガーを無効化する。
    if app_env == "production":
        debug_enabled = False

    # 明示許可がない限り、debug時の 0.0.0.0 バインドは防止する。
    if debug_enabled and host == "0.0.0.0" and not _env_flag("ALLOW_EXTERNAL_DEBUG", False):
        host = "127.0.0.1"

    app.run(host=host, port=port, debug=debug_enabled)
