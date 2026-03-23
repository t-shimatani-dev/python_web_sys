# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os
from config import Config

def setup_logger(name='employee_system'):
    """
    アプリケーションロガーのセットアップ
    
    Args:
        name (str): ロガー名
        
    Returns:
        logging.Logger: 設定済みロガー
    """
    # ログディレクトリ作成
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)
    
    # ロガー取得
    logger = logging.getLogger(name)
    
    # ログレベル設定
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 既存のハンドラをクリア（重複防止）
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # フォーマッター作成
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ファイルハンドラ（ローテーション付き）
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # ハンドラをロガーに追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# グローバルロガー初期化
app_logger = setup_logger()

if __name__ == "__main__":
    # テスト実行
    app_logger.debug("DEBUGメッセージ")
    app_logger.info("INFOメッセージ")
    app_logger.warning("WARNINGメッセージ")
    app_logger.error("ERRORメッセージ")
    app_logger.critical("CRITICALメッセージ")