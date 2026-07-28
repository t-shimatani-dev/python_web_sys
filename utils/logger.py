# utils/logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from config import Config


def setup_logger(name='employee_system', log_file=None, level=None):
    """ロガーのセットアップ。
    log_file と level が未指定の場合は config.py の Config クラスの値を使用。
    ログレベルは config.py の LOG_LEVEL で管理する。

    Args:
        name (str): ロガーの識別名。ロガーはこの名前で管理・取得される。
                    デフォルトは 'employee_system'。ルートロガーを避けるため
                    アプリ固有の名前を指定することを推奨。
        log_file (str | None): ログファイルの出力パス。
                    None の場合は Config.LOG_FILE（logs/app.log）を使用。
        level (int | None): ログレベル（例: logging.DEBUG, logging.INFO）。
                    None の場合は Config.LOG_LEVEL を文字列から定数に変換して使用。

    Returns:
        logging.Logger: ファイルハンドラーとコンソールハンドラーを設定済みの
                    ロガーオブジェクト。
    """
    # log_file が未指定の場合は Config.LOG_FILE を使用
    if log_file is None:
        log_file = Config.LOG_FILE
    # level が未指定の場合は Config.LOG_LEVEL を文字列から logging 定数に変換して使用
    if level is None:
        level = getattr(logging, Config.LOG_LEVEL, logging.INFO)

    log_dir = os.path.dirname(log_file)
    # ログディレクトリが存在しない場合は作成する
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # ロガーを取得（同一名のロガーが存在する場合はそれを再利用）
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 同一名のロガーを再利用する際に重複ハンドラーが追加されるのを防ぐ
    if logger.hasHandlers():
        logger.handlers.clear()

    # ログのフォーマットを定義
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',    # 深夜0時に切り替え
        interval=1,         # 1日ごと
        backupCount=30,     # 30日分保持
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # コンソールハンドラーも追加（開発中はコンソールにもログを出力するため）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# グローバルロガー初期化
app_logger = setup_logger()

# このファイルを直接実行した場合のみ動作確認用のテストを実行する
if __name__ == "__main__":
    # テスト実行
    app_logger.debug("DEBUGメッセージ")
    app_logger.info("INFOメッセージ")
    app_logger.warning("WARNINGメッセージ")
    app_logger.error("ERRORメッセージ")
    app_logger.critical("CRITICALメッセージ")
