# fastapi-book-sample

## 概要

FastAPIのサンプルコードです。
著者テーブルと書籍テーブルを処理できます。

- https://fastapi.tiangolo.com/ja/

## 特徴

- 5つのファイルから構成され、シンプルです。
- 非同期処理のRESTです。
- データベースはSQLiteなので、データベースのサーバーを起動することなくすぐ使えます。
- pytestのテストがあります。

## テーブル

- 著者（Author）：ID（id）、名前（name）、書籍（books）を持ちます。
- 書籍（Book）：ID（id）、名前（name）、著者ID（author_id）、著者（author）を持ちます。

## 機能

著者の機能が5つ、書籍の機能が6つ、合わせて11の機能があります。

### 著者の機能

- POST `/authors?name=...`：著者の追加
- GET `/authors`：全著者の取得
- GET `/authors/<author_id>`：特定の著者の名前取得
- PUT `/authors?author_id=...&name=...`：特定の著者の更新
- DELETE `/authors?author_id=...`：特定の著者の削除（対応する書籍も削除されます）

### 書籍の機能

- POST `/books?name=...`：書籍の追加（著者がちょうど1人必要です）
- GET `/books`：全書籍の取得
- GET `/books/<book_id>`：特定の書籍の名前取得
- GET `/books/<book_id>/details`：特定の書籍の名前と著者の取得
- PUT `/books?book_id=...&name=...`：特定の書籍の更新
- DELETE `/books?book_id=...`：特定の書籍の削除

## 構成

- main.py：FastAPIのインスタンス（app）を作成しています。
- database.py：ORMのクラスとセッションを返す関数（get_db）を定義しています。
- functions.py：データベースを処理する11機能を定義しています。
- schemas.py：RESTで扱うpydanticのクラスを定義しています。
- routers.py：パスオペレーション関数を定義しています。

## 環境構築

Python3.11で動作します。Poetryが必要です。
以下のようにしてFastAPIの仮想環境を作成します。

```
poetry install
```

## データベース初期化

以下のようにしてデータベースを初期化します。
ダミーの著者と書籍を追加しています。

```
poetry run python create_table.py
```

## FastAPIの起動

以下のようにしてFastAPIを起動します。

```
poetry run uvicorn src.main:app --host 0.0.0.0 --reload
```

## Swagger UIによるクエリ実行

下記からSwagger UIが使えます。

http://localhost:8000/docs

## 補足

- `options(selectinload(Book.author))`で著者の情報も取得しています。
- `model_config = ConfigDict(from_attributes=True)`とすることで`model_validate()`が使えます。
