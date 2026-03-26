# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='employee_system', log_file='logs/app.log', level=logging.INFO):
    """ロガーのセットアップ"""
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

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
