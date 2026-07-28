# utils/exceptions.py

class EmployeeSystemException(Exception):
    """システム共通の基底例外クラス"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseException(EmployeeSystemException):
    """データベース関連の例外"""
    pass

class ValidationException(EmployeeSystemException):
    """バリデーション関連の例外"""
    pass

class NotFoundException(EmployeeSystemException):
    """データ不存在の例外"""
    pass
