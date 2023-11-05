## 概要

[FastAPI](https://fastapi.tiangolo.com/ja/)の**シンプルなサンプルコード**の紹介です。

https://github.com/SaitoTsutomu/fastapi-book-sample

## REST APIのファイル構成

APIは`src`ディレクトリにあり、下記の5つのファイルからなります。

- `main.py`：FastAPIのインスタンス（app）を作成しています。
- `database.py`：[SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)のクラスとセッションを返す関数（get_db）を定義しています。
- `functions.py`：データベースを処理する11機能を定義しています。
- `schemas.py`：APIで扱うpydanticのクラスを定義しています。
- `routers.py`：パスオペレーション関数を定義しています。

## テーブルとカラム

APIでは、SQLiteの著者テーブルと書籍テーブルを処理します。

- 著者（Author）：ID（id）、名前（name）、書籍（books）
- 書籍（Book）：ID（id）、名前（name）、著者ID（author_id）、著者（author）

## 機能

11の機能があります。

| method | パス                          | 関数              | 説明           |
| :----- | :---------------------------- | :---------------- | :------------- |
| POST   | `/authors?name=*`             | `add_author()`    | 著者の追加     |
| GET    | `/authors`                    | `get_authors()`   | 全著者の取得   |
| GET    | `/authors/<author_id>`        | `get_author()`    | 指定著者の取得 |
| PUT    | `/authors?author_id=*&name=*` | `update_author()` | 指定著者の更新 |
| DELETE | `/authors?author_id=*`        | `delete_author()` | 指定著者の削除 |
| POST   | `/books?name=*`               | `add_book()`      | 書籍の追加     |
| GET    | `/books`                      | `get_books()`     | 全書籍の取得   |
| GET    | `/books/<book_id>`            | `get_books()`     | 指定書籍の取得 |
| GET    | `/books/<book_id>/details`    | `book_details()`  | 指定書籍の情報 |
| PUT    | `/books?book_id=*&name=*`     | `update_book()`   | 指定書籍の更新 |
| DELETE | `/books?book_id=*`            | `delete_book()`   | 指定書籍の削除 |

- 書籍を追加するには、親となる書籍が必要です
- 指定の著者を削除すると、対応する書籍も削除されます

## 環境構築

`Python 3.11`で動作します。[Poetry](https://python-poetry.org/)が必要です。
以下のようにしてFastAPIの仮想環境を作成します。

```shell
poetry install
```

## データベース初期化

以下のようにしてデータベースを初期化します。
ダミーの著者と書籍を追加しています。

```shell
poetry run python create_table.py
```

## FastAPIの起動

以下のようにしてFastAPIを起動します。

```shell
poetry run uvicorn src.main:app --host 0.0.0.0 --reload
```

## 対話的APIドキュメント

下記から[対話的APIドキュメント](https://fastapi.tiangolo.com/ja/tutorial/first-steps/#api)（Swagger UI）が使えます。

- http://localhost:8000/docs

## pytestの実行

11の機能をテストします。

```shell
poetry run pytest
```

## リレーションのデータの取得について補足

SQLAlchemy ORMの`Book`クラスは、親の`Author`のリレーション（`author`）を持っています。

```python:database.py
class Book(MappedAsDataclass, Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(Author)
```

`Book.author`の情報を取得するには、下記のように`options(selectinload(Book.author))`を使います。

```python:functions.py
async def book_details(book_id: int, db: AsyncSession) -> Book | None:
    return await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )
```

## ORMクラスからpydanticクラスへの変換の補足

下記は、指定した著者を取得するパスオペレーション関数です。

```python:routers.py
@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.get_author(author_id, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)
```

上記の`Author.model_validate(author)`では、ORMクラス（`database.Author`）から、下記のpydanticのクラス（`schemas.Author`）に変換しています。下記の`model_config = ConfigDict(from_attributes=True)`を書くことで、この変換ができるようになります。

```python:schemas.py
class Author(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
```
