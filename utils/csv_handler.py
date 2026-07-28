import csv
import logging
from typing import List, Tuple


class CSVHandler:
    """CSVファイルの読み込みとデータベースへの保存を担当するクラス"""

    def __init__(self, db_manager, validator):
        self.db_manager = db_manager
        self.validator = validator
        self.logger = logging.getLogger(__name__)

        # 必須ヘッダー列（CSVにこれらが全て存在しなければインポートエラー）
        self.required_headers = [
            '社員ID', '氏名', '氏名カナ', '部署', '役職',
            '入社日', '給与', 'メールアドレス'
        ]

    def import_from_csv(self, file_path: str) -> Tuple[int, List[str]]:
        """CSVファイルを読み込み、データベースに保存する"""
        self.logger.info(f"CSVファイルのインポートを開始: {file_path}")
        success_count = 0
        error_messages = []

        try:
            # UTF-8エンコーディングでCSVを開き、列名をキーにした辞書として行データを取得する
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # ヘッダーの検証
                if not self._validate_headers(reader.fieldnames):
                    error_message = (
                        "CSVファイルのヘッダーが不正です。"
                        f"必要なヘッダー: {self.required_headers}"
                    )
                    self.logger.error(error_message)
                    return success_count, [error_message]

                # データの検証と保存（バリデーション通過行のみDB保存し、エラー行はスキップ）
                for row_data in reader:
                    validation_errors = self.validator.validate_employee_data(
                        row_data)
                    if validation_errors:
                        error_message = (
                            f"社員ID {row_data.get('社員ID', '不明')}: "
                            + "; ".join(validation_errors)
                        )
                        self.logger.warning(error_message)
                        error_messages.append(error_message)
                        continue

                    try:
                        self.db_manager.save_employee(row_data)
                        success_count += 1
                    except Exception as e:
                        error_message = (
                            f"社員ID {row_data.get('社員ID', '不明')}: "
                            f"データベースへの保存に失敗 - {str(e)}"
                        )
                        self.logger.error(error_message)
                        error_messages.append(error_message)

        except FileNotFoundError:
            error_message = f"ファイルが見つかりません: {file_path}"
            self.logger.error(error_message)
            return success_count, [error_message]
        except Exception as e:
            error_message = f"CSVファイルの読み込み中にエラーが発生: {str(e)}"
            self.logger.error(error_message)
            return success_count, [error_message]

        self.logger.info(
            f"CSVファイルのインポートが完了しました。成功: {success_count}, "
            f"エラー: {len(error_messages)}"
        )
        return success_count, error_messages

    def _validate_headers(self, headers) -> bool:
        """CSVヘッダーの検証"""
        if not headers:
            return False
        # required_headers の全要素が fieldnames に含まれているか一括確認
        return all(
            header_row_data in headers
            for header_row_data in self.required_headers
        )
