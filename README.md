# 社員情報管理システム - Python学習プロジェクト

Python3の基本文法を学習するための実践的なWebアプリケーション開発プロジェクトです。

## 📋 プロジェクト概要

### 目的
- Python3の基本文法を実践的に学習
- Webアプリケーション開発の基礎を習得
- データベース操作、ファイル操作、エラー処理などの実装パターンを理解

### 想定工数
約10時間

### 主な機能
- ✅ CSVファイルからのデータインポート
- ✅ 社員情報のCRUD操作（作成・読み取り・更新・削除）
- ✅ 検索機能（複数条件対応）
- ✅ データバリデーション
- ✅ エラーハンドリングとログ出力

---

## 🎯 学習できるPython3文法

### 基本構文
- ✅ 変数、データ型（int, float, str, bool, None）
- ✅ コメント、docstring
- ✅ インデント

### 演算子
- ✅ 四則演算（+, -, *, /）
- ✅ 除算（//, %）、べき乗（**）
- ✅ 比較演算子（==, !=, <, >, <=, >=）
- ✅ 論理演算子（and, or, not）
- ✅ 代入演算子（=, +=, -=）

### 制御構文
- ✅ if, elif, else
- ✅ for文、while文
- ✅ break, continue, pass

### データ構造
- ✅ リスト、タプル、辞書、セット
- ✅ リスト内包表記

### 関数とクラス
- ✅ 関数定義（def）
- ✅ 引数（位置引数、キーワード引数、デフォルト引数）
- ✅ 戻り値
- ✅ lambda式
- ✅ クラス定義、継承
- ✅ コンストラクタ（__init__）

### 例外処理
- ✅ try, except, finally
- ✅ raise
- ✅ カスタム例外

### ファイル・データ操作
- ✅ ファイル読み書き（open, with文）
- ✅ CSVファイル操作
- ✅ SQLiteデータベース操作
- ✅ 正規表現（re module）
- ✅ 日付操作（datetime）

### モジュール
- ✅ import文
- ✅ from ... import
- ✅ __name__ == "__main__"

---

## 📁 ドキュメント構成

| ファイル名 | 説明 | 参照タイミング |
|----------|------|--------------|
| [機能設計書.md](機能設計書.md) | システム全体の機能仕様 | 最初に全体像を把握 |
| [詳細設計書.md](詳細設計書.md) | 詳細設計書（D-00～D-10 全機能） | 実装時に参照 |
| [実装手順書.md](実装手順書.md) | ステップバイステップの実装手順 | 実装中に随時参照 |
| README.md（本ファイル） | プロジェクト概要とクイックスタート | 最初に読む |

### ドキュメント間の関係

README.md（エントリーポイント）  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
機能設計書.md（システム全体の理解）  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
実装手順書.md（実装の進め方）  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
詳細設計書.md（実装詳細・全機能統合版）

---

## 🚀 クイックスタート

### 0. 開発環境ポリシー（uvベース）

- 本プロジェクトは、想定技術（Python 3.10+/Flask/SQLite3/Jinja2）を維持したまま、依存関係管理と仮想環境管理を uv に統一します。
- 依存関係は pyproject.toml と uv.lock で固定し、ローカル実行とDocker実行の再現性を確保します。
- 既存の pip/venv 手順は互換運用向けの参考情報とし、新規セットアップは uv 手順を優先してください。

### 1. 環境構築（5分・uv推奨）

\`\`\`bash
# プロジェクトディレクトリに移動
cd /home/agio0021/projects/python_web_sys

# 依存関係同期（.venv も自動作成）
uv sync

# アプリ起動
uv run python app.py
\`\`\`

### 1.1 既存手順（pip/venv、互換運用向け）

### 1. 環境構築（5分）

\`\`\`bash
# プロジェクトディレクトリに移動
cd /home/agio0021/projects/python_web_sys

# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate

# 依存パッケージインストール
pip install Flask==3.0.0 python-dateutil==2.8.2
\`\`\`

### 2. ディレクトリ作成（1分）

\`\`\`bash
# 必要なディレクトリを作成
mkdir -p database utils routes templates/employees static/css static/js data logs tests

# Pythonパッケージ化
touch database/__init__.py utils/__init__.py routes/__init__.py
\`\`\`

### 3. サンプルCSV作成（1分）

<pre><code class="language-bash">cat > data/sample_employees.csv << 'EOF'
社員ID,氏名,氏名カナ,部署,役職,入社日,給与,メールアドレス
A0001,山田太郎,ヤマダタロウ,営業部,部長,2010-04-01,8000000,yamada@example.com
A0002,佐藤花子,サトウハナコ,開発部,課長,2015-07-15,6500000,sato@example.com
A0003,鈴木一郎,スズキイチロウ,総務部,一般,2020-04-01,4000000,suzuki@example.com
A0004,田中美咲,タナカミサキ,人事部,係長,2018-10-01,5000000,tanaka@example.com
A0005,高橋健太,タカハシケンタ,経理部,主任,2019-01-15,4500000,takahashi@example.com
EOF
</code></pre>

### 4. 実装開始

**[実装手順書.md](実装手順書.md)** を開いて、ステップ1から順に実装を進めてください。

### 5. Dockerサンプル設定（uvベース）

以下の Docker 関連ファイルをサンプルとして追加しています。

- Dockerfile
  - ベースイメージ: python:3.12-slim
  - uv を公式イメージからコピーして利用
  - pyproject.toml と uv.lock を使って uv sync --frozen --no-dev を実行
  - コンテナ起動時に uv run python app.py で Flask アプリを起動

- docker-compose.yml
  - サービス名 web
  - 5000:5000 をポート公開
  - 起動コマンドは uv run python app.py

- .dockerignore
  - .git、venv、.venv、__pycache__、logs/ などを除外
  - ビルドコンテキストを小さくし、ビルド時間短縮と不要ファイル混入防止を目的

#### Docker 実行例

```bash
# イメージをビルド
docker build -t python-web-sys:uv .

# コンテナ起動
docker run --rm -p 5000:5000 python-web-sys:uv
```

```bash
# または compose で起動
docker compose up --build
```

---

## 📊 進捗管理

### 全体進捗（チェックボックス形式）

#### 環境構築
- [ ] uv sync で依存関係同期
- [ ] uv run python app.py で起動確認
- [ ] ディレクトリ構成作成

#### 実装（詳細は[実装手順書.md](実装手順書.md)参照）
- [ ] ステップ1: 設定ファイル（15分）
- [ ] ステップ2: ロガー（30分）
- [ ] ステップ3: データベース管理（45分）
- [ ] ステップ4: バリデーション（1時間）
- [ ] ステップ5: CSVハンドラ（1.5時間）
- [ ] ステップ6: Flaskベース（30分）
- [ ] ステップ7: テンプレート（1時間）
- [ ] ステップ8: 社員一覧機能（1時間）
- [ ] ステップ9: 社員詳細機能（30分）
- [ ] ステップ10: 社員登録機能（1.5時間）
- [ ] ステップ11: 社員更新機能（1時間）
- [ ] ステップ12: 社員削除機能（30分）
- [ ] ステップ13: 社員検索機能（1.5時間）
- [ ] ステップ14: スタイリング（30分・オプション）

#### テスト
- [ ] 単体テスト実施
- [ ] 統合テスト実施（全10項目）

---

## 変更履歴

| 版数 | 日付 | 変更内容 | 作成者 |
|-----|------|---------|-------|
| 1.0 | 2026-03-22 | 初版作成 | - |
