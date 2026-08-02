# uvベース移行手順書（ローカル + Docker）

本手順書は、既存の venv + pip + requirements.txt 運用を、uv ベース運用へ置き換えるための実行手順です。

対象プロジェクト: path/to/python_web_sys

---

## 0. 事前準備

### 目的
- 現状を壊さずに移行できる状態を作る

### 実施コマンド
```bash
cd /home/agio0021/projects/python_web_sys
git status
git checkout -b chore/migrate-to-uv
```

### 成功確認
- git status で現在の変更状態を確認できる
- git checkout -b 実行後、作業ブランチへ切り替わる

### 判定基準
- 成功: ブランチ名が chore/migrate-to-uv になっている
- 失敗: ブランチ切り替えエラーが出る（権限・未コミット競合など）

### チェック
- [ ] 事前準備を完了

---

## 1. uv の導入確認

### 目的
- uv コマンドが利用可能であることを確認する

### 実施コマンド
```bash
uv --version
```

### 成功確認
- バージョン文字列（例: uv 0.x.x）が表示される

### 判定基準
- 成功: バージョン表示あり
- 失敗: uv: command not found など

### 失敗時対応
<pre><code class="language-bash"># 例: インストールスクリプトを保存し、内容を確認してから実行
curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh
sh install-uv.sh
rm -f install-uv.sh
exec "$SHELL"
uv --version
</code></pre>

### チェック
- [ ] uv が利用可能

---

## 2. 現行依存関係の確認

### 目的
- 既存の依存セットを移行対象として明確化する

### 実施コマンド
```bash
cat requirements.txt
```

### 成功確認
- Flask==3.0.0 などの依存一覧が表示される

### 判定基準
- 成功: requirements が読み取れる
- 失敗: ファイルなし/空ファイル

### チェック
- [ ] 現行依存関係を確認

---

## 3. pyproject.toml を初期化

### 目的
- uv 運用の基準ファイルを作成する

### 実施コマンド
```bash
cd /home/agio0021/projects/python_web_sys
uv init --bare --python 3.10
```

### 成功確認
- ルートに pyproject.toml が作成される

### 判定基準
- 成功: pyproject.toml が存在し、requires-python = ">=3.10" が設定されている
- 失敗: 既存ファイル競合や初期化エラー

### 確認コマンド
```bash
ls -la pyproject.toml
cat pyproject.toml
```

### チェック
- [ ] pyproject.toml を作成

---

## 4. requirements.txt から依存を取り込む

### 目的
- 既存依存を uv 管理下へ移行する

### 実施コマンド
```bash
uv add -r requirements.txt
```

### 成功確認
- pyproject.toml の dependencies に依存が追加される

### 判定基準
- 成功: dependencies に必要パッケージが含まれる
- 失敗: 依存解決エラー（バージョン競合など）

### 確認コマンド
```bash
cat pyproject.toml
```

### チェック
- [ ] 依存取り込みを完了

---

## 5. lock 作成と仮想環境同期

### 目的
- 再現性のある依存解決結果を固定し、実環境へ同期する

### 実施コマンド
```bash
uv lock
uv sync
```

### 初心者向け解説（uv lock と uv sync の違い）

- uv lock は、依存関係の設計図を確定するコマンドです。
- pyproject.toml の条件をもとに、実際に使うパッケージとバージョンの組み合わせを決定し、uv.lock に保存します。
- これにより、別のPCや別メンバーでも同じ依存関係を再現しやすくなります。

- uv sync は、uv.lock の内容に合わせて実際の環境（.venv）を整えるコマンドです。
- 足りないパッケージはインストールし、不要な差分は整理して、環境を lock の状態に一致させます。

#### 使う順番
1. pyproject.toml を編集（依存追加・変更）
2. uv lock で固定情報を更新
3. uv sync で実環境へ反映

#### Ubuntu起動ごとの扱い
- `uv sync` は、Ubuntuを起動するたびに毎回実行するものではありません。
- 通常は、初回セットアップ時と、`pyproject.toml` や `uv.lock` を変更したあとに実行します。
- `.venv` がすでにあり、依存関係に変更がないなら、起動時は `uv run python app.py` だけで十分です。
- つまり、`uv sync` は「環境を揃え直す作業」であって、「毎回の起動コマンド」ではありません。

#### 実行ルール（複数Pythonファイルを作成する場合）
- 依存パッケージを使う実行は、`uv run` 経由を原則とします。
- 単体スクリプトを直接実行する場合は、`uv run python XXX.py` を使います。
- パッケージ配下のモジュールを実行する場合は、`uv run python -m package.module` を使います。
- `package.module` は、`package/` ディレクトリ内の `module.py` をドット区切りで指定する実行方法です。
- 例:
  - `uv run python import_csv.py`
  - `uv run python -m routes.employee_routes`

#### イメージ（たとえ）
- pyproject.toml: 欲しい材料の希望リスト
- uv lock: 実際に買う材料を品番まで確定した買い物メモ
- uv sync: 買い物メモどおりにキッチンへ材料をそろえる作業


### 成功確認
- uv.lock と .venv/ が作成される

### 判定基準
- 成功: uv.lock 存在 + .venv 存在
- 失敗: lock/sync エラー

### 確認コマンド
```bash
ls -la uv.lock
ls -la .venv
```

### チェック
- [ ] lock と sync を完了

---

## 6. アプリ実行確認（uv run）

### 目的
- uv 環境でアプリが正常起動することを確認する

### 実施コマンド
```bash
uv run python app.py
```

別ターミナルで確認:
```bash
curl -I http://127.0.0.1:5000/
```

### 成功確認
- 起動ログにエラーがない
- curl の応答で HTTP/1.1 200 または 302 が返る

### 判定基準
- 成功: アプリ起動 + HTTP 応答確認
- 失敗: 起動例外、ポート競合、500 応答

### チェック
- [ ] uv run で起動確認

---

## 6.1 トラブルシュート（No module named "flask"）

### 症状

```bash
PYTHONPATH=. python3 app.py
# ModuleNotFoundError: No module named "flask"
```

### 根本原因

- システム Python（例: /usr/bin/python3）で起動しており、依存関係が入った仮想環境を使えていないためです。

### 対処手順（推奨）

```bash
# 依存関係を同期
uv sync

# uv管理の環境で起動
uv run python app.py
```

### 代替手順（互換運用）

```bash
source venv/bin/activate
python3 app.py
```

### 確認コマンド

```bash
which python3
python3 -c "import sys; print(sys.executable)"
```

- /usr/bin/python3 が表示される場合は、仮想環境が有効になっていません。

---

## 7. ドキュメント運用切替

### 目的
- 開発手順の公式運用を uv に統一する

### 実施内容
- README と 実装手順書で uv 手順を優先記載
- 旧 venv/pip は互換情報として残す

### 成功確認
- ドキュメントに uv sync と uv run が明記されている

### 判定基準
- 成功: 参照ドキュメントの手順が uv 優先
- 失敗: 旧手順のみのまま

### チェック
- [ ] ドキュメント整合を確認

---

## 8. Docker を uv ベースへ切り替え

### 目的
- コンテナ内でもローカルと同じ依存セットで実行する

### 前提
- このリポジトリに Dockerfile が未作成の場合は新規作成する

### Dockerfile 作成例
```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 5000
CMD ["uv", "run", "python", "app.py"]
```

### （任意）docker-compose.yml 作成例
```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./:/app
    command: ["uv", "run", "python", "app.py"]
```

### 成功確認
```bash
docker build -t python-web-sys:uv .
docker run --rm -p 5000:5000 python-web-sys:uv
```

### 5000 番ポートが使用中の場合の手順
1. 5000 番を使っている既存コンテナを確認する。
```bash
docker ps --filter "publish=5000" --format "{{.Names}} {{.Status}} {{.Ports}}"
```
2. 該当コンテナがあれば停止する。
```bash
docker stop <container_name>
```
3. Docker 以外のプロセスが 5000 番を使っていないか確認する。
```bash
ss -ltnp | grep ':5000'
```
4. プロセスが見つかった場合は PID を確認して停止する。
```bash
kill <PID>
```
5. 停止後に、もう一度 Docker コンテナを起動する。
```bash
docker run --rm -p 5000:5000 python-web-sys:uv
```

### 実行結果の確認手順
別ターミナルで次を実行する。
```bash
curl -I http://127.0.0.1:5000/
```

5000 番が空いている状態で実行する。

### 成否の確認基準
- 成功: `HTTP/1.1 200 OK` または `HTTP/1.1 302 FOUND` が返る
- 失敗: `Recv failure: 接続が相手からリセットされました`、`Connection refused`、または応答なし

### チェック
- [ ] Docker を uv ベースへ切り替え

## 9. 旧 venv の扱い

### 目的
- uv 移行後の混在事故を防止する

### 実施内容
- 1〜8 がすべて成功するまでは venv/ を保持
- 完全移行後に不要なら削除

### 実施コマンド（削除する場合のみ）
```bash
rm -rf venv
```

### 成功確認
- venv が削除され、uv sync → uv run で問題なく動く

### 判定基準
- 成功: 旧 venv なしで再現可能
- 失敗: 旧 venv 前提のコマンドが残っている

### チェック
- [ ] 旧 venv の扱いを決定

---

## 10. 最終確認チェックリスト

- [ ] uv --version が通る
- [ ] pyproject.toml が存在し Python 3.10+ 制約がある
- [ ] uv.lock が存在する
- [ ] uv sync が成功する
- [ ] uv run python app.py で起動できる
- [ ] http://127.0.0.1:5000/ にアクセスできる
- [ ] Docker build/run が成功する（Docker運用する場合）
- [ ] README / 実装手順書が uv 方針に整合している

---

## 参考: よくあるエラーと対処

1. uv sync で依存解決失敗
- 対処: uv lock --upgrade を実施し、競合パッケージを確認

2. uv run python app.py で ModuleNotFoundError
- 対処: uv sync の再実行、pyproject.toml の dependencies を確認

3. Docker で起動するが 500 エラー
- 対処:
```bash
docker logs <container_id>
```

4. ポート競合（5000 使用中）
- 対処:
```bash
docker run --rm -p 5001:5000 python-web-sys:uv
```
