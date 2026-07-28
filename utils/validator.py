# utils/validator.py
import re
from datetime import datetime
from typing import Tuple


class DataValidator:
    """データバリデーションクラス"""

    # 正規表現パターン
    EMPLOYEE_ID_PATTERN = re.compile(r'^[A-Z][0-9]{4}$')
    NAME_KANA_PATTERN = re.compile(r'^[ァ-ヴー\s　]+$')
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^[0-9-]+$')
    POSTAL_CODE_PATTERN = re.compile(r'^\d{3}-\d{4}$')
    HIRE_DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    # 定義済み選択肢
    VALID_DEPARTMENTS = ['営業部', '開発部', '総務部', '人事部', '経理部']
    VALID_POSITIONS = ['部長', '課長', '係長', '主任', '一般']

    def validate_employee_id(self, employee_id: str) -> Tuple[bool, str]:
        """社員IDのバリデーション"""
        if not employee_id:
            return False, "社員IDは必須です"
        if not self.EMPLOYEE_ID_PATTERN.match(employee_id):
            return False, "社員IDは英字1文字+数字4桁の形式です（例: A0001）"
        return True, ""

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """氏名のバリデーション"""
        if not name or not name.strip():
            return False, "氏名は必須です"
        if len(name) > 50:
            return False, "氏名は50文字以内です"
        return True, ""

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """メールアドレスのバリデーション"""
        if not email:
            return False, "メールアドレスは必須です"
        if len(email) > 255:
            return False, "メールアドレスは255文字以内です"
        if not self.EMAIL_PATTERN.match(email):
            return False, "正しいメールアドレス形式で入力してください"
        return True, ""

    def validate_hire_date(self, hire_date: str) -> Tuple[bool, str]:
        """入社日のバリデーション"""
        if not hire_date:
            return False, "入社日は必須です"
        if not self.HIRE_DATE_PATTERN.match(hire_date):
            return False, "入社日はYYYY-MM-DD形式で入力してください"

        try:
            date_obj = datetime.strptime(hire_date, '%Y-%m-%d')
            if date_obj.year < 1900:
                return False, "入社日は1900年以降の日付を入力してください"
            if date_obj > datetime.now():
                return False, "入社日は今日以前の日付を入力してください"
        except ValueError:
            return False, "正しい日付を入力してください"

        return True, ""

    def validate_salary(self, salary: str) -> Tuple[bool, str]:
        """給与のバリデーション"""
        if not salary:
            return False, "給与は必須です"
        try:
            salary_int = int(salary)
            if salary_int < 0:
                return False, "給与は0以上の整数です"
            if salary_int > 999999999:
                return False, "給与は999,999,999以下です"
        except ValueError:
            return False, "給与は整数で入力してください"
        return True, ""

    def validate_name_kana(self, name_kana: str) -> Tuple[bool, str]:
        """氏名カナのバリデーション"""
        if not name_kana or not name_kana.strip():
            return False, "氏名カナは必須です"
        if not self.NAME_KANA_PATTERN.match(name_kana):
            return False, "氏名カナは全角カタカナで入力してください"
        if len(name_kana) > 50:
            return False, "氏名カナは50文字以内です"
        return True, ""

    def validate_department(self, department: str) -> Tuple[bool, str]:
        """部署のバリデーション"""
        if not department:
            return False, "部署は必須です"
        if department not in self.VALID_DEPARTMENTS:
            return False, f"部署は次のいずれかを選択してください: {
                ', '.join(
                    self.VALID_DEPARTMENTS)}"
        return True, ""

    def validate_position(self, position: str) -> Tuple[bool, str]:
        """役職のバリデーション"""
        if not position:
            return False, "役職は必須です"
        if position not in self.VALID_POSITIONS:
            return False, f"役職は次のいずれかを選択してください: {
                ', '.join(
                    self.VALID_POSITIONS)}"
        return True, ""

    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """電話番号のバリデーション（オプション項目）"""
        if not phone or not phone.strip():
            return True, ""  # 空欄OK
        if not self.PHONE_PATTERN.match(phone):
            return False, "電話番号は数字とハイフンのみ入力可能です"
        if len(phone) > 20:
            return False, "電話番号は20文字以内です"
        return True, ""

    def validate_postal_code(self, postal_code: str) -> Tuple[bool, str]:
        """郵便番号のバリデーション（オプション項目）"""
        if not postal_code or not postal_code.strip():
            return True, ""  # 空欄OK
        if not self.POSTAL_CODE_PATTERN.match(postal_code):
            return False, "郵便番号は123-4567形式で入力してください"
        return True, ""

    def validate_address(self, address: str) -> Tuple[bool, str]:
        """住所のバリデーション（オプション項目）"""
        if not address or not address.strip():
            return True, ""  # 空欄OK
        if len(address) > 255:
            return False, "住所は255文字以内です"
        return True, ""

    def validate_notes(self, notes: str) -> Tuple[bool, str]:
        """備考のバリデーション（オプション項目）"""
        if not notes or not notes.strip():
            return True, ""  # 空欄OK
        if len(notes) > 1000:
            return False, "備考は1000文字以内です"
        return True, ""

    def validate_employee_data(self, data: dict) -> list:
        """社員データの総合バリデーション（必須8項目を一括チェック）"""
        errors = []
        checks = [
            (self.validate_employee_id, data.get('社員ID', '')),
            (self.validate_name, data.get('氏名', '')),
            (self.validate_name_kana, data.get('氏名カナ', '')),
            (self.validate_department, data.get('部署', '')),
            (self.validate_position, data.get('役職', '')),
            (self.validate_email, data.get('メールアドレス', '')),
            (self.validate_hire_date, data.get('入社日', '')),
            (self.validate_salary, data.get('給与', '')),
        ]
        for validator_func, value in checks:
            is_valid, message = validator_func(value)
            if not is_valid:
                errors.append(message)
        return errors


if __name__ == "__main__":
    # テスト実行
    validator = DataValidator()

    print("=== 必須項目のバリデーションテスト ===")
    # 正常ケース
    tests = [
        ("社員ID", validator.validate_employee_id, "A0001"),
        ("氏名", validator.validate_name, "山田太郎"),
        ("氏名カナ", validator.validate_name_kana, "ヤマダタロウ"),
        ("部署", validator.validate_department, "営業部"),
        ("役職", validator.validate_position, "部長"),
        ("メール", validator.validate_email, "test@example.com"),
        ("入社日", validator.validate_hire_date, "2020-01-01"),
        ("給与", validator.validate_salary, "5000000"),
    ]

    for label, func, value in tests:
        valid, msg = func(value)
        status = "✓" if valid else "✗"
        print(f"{status} {label}: {value} - {msg if msg else 'OK'}")

    print("\n=== オプション項目のバリデーションテスト ===")
    optional_tests = [
        ("電話番号", validator.validate_phone, "03-1234-5678"),
        ("郵便番号", validator.validate_postal_code, "123-4567"),
        ("住所", validator.validate_address, "東京都千代田区1-1"),
        ("備考", validator.validate_notes, "特になし"),
    ]

    for label, func, value in optional_tests:
        valid, msg = func(value)
        status = "✓" if valid else "✗"
        print(f"{status} {label}: {value} - {msg if msg else 'OK'}")

    print("\n=== エラーケースのテスト ===")
    error_tests = [
        ("社員ID不正", validator.validate_employee_id, "0001"),
        ("カナ不正", validator.validate_name_kana, "yamada"),
        ("部署不正", validator.validate_department, "不明部署"),
        ("給与負数", validator.validate_salary, "-1000"),
    ]

    for label, func, value in error_tests:
        valid, msg = func(value)
        status = "✓" if valid else "✗"
        print(f"{status} {label}: {value} - {msg}")
