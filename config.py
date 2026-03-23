# config.py
import os

class Config:
    """アプリケーション設定"""
    
    # Flask設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # データベース設定
    DATABASE_PATH = 'database/employees.db'
    
    # ログ設定
    LOG_DIR = 'logs'
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_LEVEL = 'INFO'
    
    # アプリケーション設定
    APP_NAME = '社員情報管理システム'
    VERSION = '1.0.0'