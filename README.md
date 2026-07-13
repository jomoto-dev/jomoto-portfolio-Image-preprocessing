# Image Preprocessing API

レシート画像や書類画像を、OCRなどの後続処理で扱いやすい形に変換するための画像前処理APIです。
画像をアップロードすると、グレースケール化・二値化・保存・プレビュー・ダウンロードまでをFastAPI上で実行できます。

## 作成背景

Pythonを用いた画像認識・OCR関連の実務を想定し、グレースケール化や二値化といった基本的な前処理を行うAPIを作成しました。
また、画像処理だけでなく、Web APIとしての入力チェック、レスポンス設計、Pydanticによるレスポンス定義、pytestによる基本的なテストまで意識して実装しました。

## 開発方針

このアプリは、AIツールを設計相談・実装補助・エラー調査・README整理の補助として活用しながら開発しました。
ただし、生成されたコードをそのまま使うのではなく、FastAPIによる画像アップロード処理、OpenCVによるグレースケール化・二値化、レスポンス設計、テスト内容を確認し、自分で動作検証しながら実装を進めました。

DB・認証・フロントエンドはあえて追加せず、画像アップロード、画像処理、ファイル保存、レスポンス設計、テストに絞って実装しています。
機能を増やしすぎるよりも、APIとしての基本処理を理解し、面接で説明できる構成にすることを重視しました。

## デモイメージ

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/f468d3ea-a2a6-4561-ac33-49eb03c23e13" />

<table>
  <tr>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/20581efc-5caf-4608-bd92-5562ec113d85" />処理前</td>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/bae28c12-5361-4651-8366-c073833151be" />グレースケール</td>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/57499649-a0be-4ce4-978e-3eb4d162d235" />二値</td>
  </tr>
</table>

## 使用技術と選定理由

| 分類 | 技術 | 採用理由 |
|---|---|---|
| 言語 | Python | 高性能な画像処理ライブラリ（OpenCV）の充実度と、高速なAPI開発を両立させるため |
| API | FastAPI | Swagger UIが自動生成され、APIの動作確認や仕様確認がしやすいため |
| レスポンス定義 | Pydantic | APIレスポンスの型を定義し、Swagger UI上でレスポンス仕様を分かりやすく表示するため |
| 画像処理 | OpenCV | グレースケール化・二値化などの基本的な画像前処理を実装しやすいため |
| GIF読み込み | Pillow | GIFの先頭フレームを画像として読み込むため |
| サーバー | Uvicorn | FastAPIアプリをローカル環境で起動するため |

## API一覧

| メソッド | エンドポイント | 役割 |
|---|---|---|
| GET | `/` | APIの起動確認 |
| POST | `/process-image` | 画像をアップロードして前処理する |
| GET | `/preview/{filename}` | 処理済み画像をブラウザで表示する |
| GET | `/download/{filename}` | 処理済み画像をダウンロードする |

## セットアップ方法

```
#クローン作製
git clone https://github.com/jomoto-dev/jomoto-portfolio-Image-preprocessing.git
cd image-preprocessing-api

#仮想環境の作成
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# インストール
python -m pip install -r requirements.txt
```

その後以下の方法で起動します。
```
python -m uvicorn main:app --reload
```

起動後のアクセス<br>
<http://127.0.0.1:8000/docs>

## 使い方
1. アプリを起動し、ブラウザで<http://127.0.0.1:8000/docs>にアクセスする
2. Swagger UIから`POST /process-image`を開く
3. `Try it out`をクリックし、処理したい画像を選択する
4. `Execute`を押すと画像が処理される
5. `Response body`の`results`内にある`preview_url`から処理済み画像を確認したり、`download_url`から画像をダウンロードしたりできる

## 実装した機能

- 画像アップロード
- OpenCVによるグレースケール化
- OpenCVによる二値化
- outputフォルダへの画像保存
- JSONレスポンス返却
- Pydantic response model によるレスポンス仕様の明確化
- Swagger UIでの動作確認

## 各機能の仕様紹介

### 画像アップロード

- `POST /process-image` から画像をアップロードできます。  
- 対応形式は jpg / jpeg / png / gif、最大ファイルサイズは5MBです。  
- GIFは先頭フレームのみ処理します。アニメーションGIFの全フレーム処理は行いません。
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/edec0639-38c1-4b0b-a1a4-559491aa5d38" />

### 処理モード指定

プルダウンから選択することで、`mode`で前処理の指定ができます。
- `grayscale`: グレースケール化した画像を保存します。
- `binary`: グレースケール化した後、二値化した画像を保存します。
- `both`: グレースケール画像と二値化画像の両方を保存します。

（`mode` を指定しない場合は、`binary` として処理されます。）
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/950c888c-9e7d-49c7-bc93-c2fa4c3000b5" />

### 保存形式指定

プルダウンから選択することで、`output_format`で保存形式の指定ができます。

- `png`: png形式で保存します。
- `jpg`: jpg形式で保存します。

（`output_format` を指定しない場合は、`png` として保存されます。）<br>
（GIFをアップロードした場合も、出力は `png` または `jpg` で保存されます。）
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/ec071dd4-2d8c-40d8-8572-792190b70e1c" />

### 処理済み画像のダウンロード

処理済み画像は、`GET /download/{filename}` でダウンロードできます。<br>
`/process-image` の `results` 内には `download_url` も含まれるため、そのURLから直接ダウンロードすることもできます。<br>
例:

```text
GET http://127.0.0.1:8000/download/processed_binary_xxxxx.png
↑APIのresponseに表示されているURLをブラウザに入力する
```

<img width="800" alt="Image" src="https://github.com/user-attachments/assets/f1846b0e-dbcd-46fd-a9dd-638056ce3250" />
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/7b8d8562-a9de-4556-af1d-3bbc35447163" />

### 処理済み画像のプレビュー

処理済み画像は、`GET /preview/{filename}` でブラウザ上に表示できます。<br>
レスポンスの `results` 内にある `preview_url` を使うと、処理済み画像をブラウザでも確認できます。<br>
例:

```text
GET http://127.0.0.1:8000/preview/processed_binary_xxxxx.png
↑APIのresponseに表示されているURLをブラウザに入力する
```

<img width="800" alt="Image" src="https://github.com/user-attachments/assets/c7b8580f-e1d9-4092-94c0-c91930bde556" />
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/7b8d8562-a9de-4556-af1d-3bbc35447163" />


## API仕様

### エンドポイント一覧

| メソッド | エンドポイント | 内容 |
|---|---|---|
| GET | `/` | APIの起動確認 |
| POST | `/process-image` | 画像をアップロードして前処理を実行 |
| GET | `/download/{filename}` | 処理済み画像をダウンロード |
| GET | `/preview/{filename}` | 処理済み画像をブラウザで表示 |

### GET /

#### 入力

なし

#### レスポンス

APIが起動していることを確認するためのJSONを返します。

| フィールド | 説明 |
|---|---|
| `message` | APIの起動状態を表すメッセージ |

#### レスポンス例

```json
{
  "message": "Image Preprocessing API is running"
}
```

### POST /process-image

#### 入力

| パラメータ | 種類 | 必須 | 説明 |
|---|---|---|---|
| `file` | file | 必須 | アップロードする画像ファイル |
| `mode` | form | 任意 | `grayscale` / `binary` / `both` から選択。省略時は `binary` |
| `output_format` | form | 任意 | `png` / `jpg` から選択。省略時は `png` |

#### レスポンス

`/process-image` のレスポンスでは、処理結果を常に `results` 配列で返します。

| フィールド | 説明 |
|---|---|
| `message` | 処理結果メッセージ |
| `mode` | 実行した処理モード |
| `output_format` | 保存形式 |
| `steps` | 実行した処理ステップ |
| `results` | 処理済み画像の情報配列 |

`results` の各要素には以下の情報が含まれます。

| フィールド | 説明 |
|---|---|
| `type` | `grayscale` または `binary` |
| `filename` | 保存されたファイル名 |
| `output_path` | 保存先のパス |
| `preview_url` | ブラウザ表示用URL |
| `download_url` | ダウンロード用URL |

#### レスポンス例

```json
{
  "message": "Image processed successfully",
  "mode": "binary",
  "output_format": "png",
  "steps": [
    "uploaded",
    "converted_to_grayscale",
    "applied_threshold",
    "saved_output_image"
  ],
  "results": [
    {
      "type": "binary",
      "filename": "processed_binary_xxxxx.png",
      "output_path": "output/processed_binary_xxxxx.png",
      "preview_url": "/preview/processed_binary_xxxxx.png",
      "download_url": "/download/processed_binary_xxxxx.png"
    }
  ]
}
```

### GET /download/{filename}

#### 入力

| パラメータ | 種類 | 必須 | 説明 |
|---|---|---|---|
| `filename` | path | 必須 | `POST /process-image` の `results[].filename` で返されたファイル名 |

#### レスポンス

成功時は、処理済み画像をダウンロード用のファイルとして返します。

| 項目 | 内容 |
|---|---|
| ステータスコード | `200` |
| レスポンス本文 | 画像ファイルのデータ |
| Content-Type | `image/png` または `image/jpeg` |

#### レスポンス例

```text
200 OK
Content-Type: image/png
Content-Disposition: attachment; filename="processed_binary_xxxxx.png"

PNG画像データ
```

### GET /preview/{filename}

#### 入力

| パラメータ | 種類 | 必須 | 説明 |
|---|---|---|---|
| `filename` | path | 必須 | `POST /process-image` の `results[].filename` で返されたファイル名 |

#### レスポンス

成功時は、処理済み画像をブラウザ表示用のファイルとして返します。

| 項目 | 内容 |
|---|---|
| ステータスコード | `200` |
| レスポンス本文 | 画像ファイルのデータ |
| Content-Type | `image/png` または `image/jpeg` |

#### レスポンス例

```text
200 OK
Content-Type: image/png

PNG画像データ
```

### 主なエラーコード
| ステータスコード | 発生条件                             |
| -------- | -------------------------------- |
| 400      | 非対応形式のファイルをアップロードした場合            |
| 400      | 空ファイルをアップロードした場合                 |
| 400      | 5MBを超えるファイルをアップロードした場合           |
| 404      | 存在しない処理済み画像をプレビュー・ダウンロードしようとした場合 |



## ディレクトリ構成

```text
image-preprocessing-api/
├─ main.py
├─ requirements.txt
├─ README.md
├─ output/
└─ tests/
   └─ test_main.py
```
* 各ファイルの関係性を表した図
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/8410a1f3-a8af-4d75-9db6-7db4b020a0e4" />

## テスト実行方法

以下のコマンドでテストを実行できます。

```
python -m pytest
```
期待される結果:

```text
4 passed
```

## 実装時に工夫した点

1. **`mode` と `output_format` を選択式にした**

   `mode` はグレースケール化・二値化・両方保存から選べるようにし、`output_format` は `png` / `jpg` から選択できるようにしました。手入力ミスを減らし、Swagger UI上でも動作確認しやすい形にしています。

2. **`results` 配列でレスポンス形式を統一した**

   1枚だけ保存する場合も、複数画像を保存する場合も、常に `results` 配列で返すようにしました。処理モードによってレスポンス構造が変わらないため、利用側で結果を扱いやすくしています。

3. **Pydantic response model を追加した**

   返却するJSONの形をPydanticで定義し、Swagger UI上でもレスポンス仕様を確認できるようにしました。`message` や `results` など、返ってくる項目が分かりやすくなるよう意識しています。

4. **拡張子とファイルサイズを制限した**

   画像以外のファイルや大きすぎるファイルを受け付けると、処理失敗や負荷増加につながるため、対応形式とファイルサイズを事前にチェックし、不正な入力には400エラーを返すようにしました。

5. **`output` フォルダ外にアクセスされないよう安全なパスチェックを入れた**

   プレビューやダウンロードでは、ユーザーが指定したファイル名をそのまま信用しないようにしました。`output` フォルダ内のファイルだけを返すことで、意図しないファイル参照を防いでいます。

6. **pytestで基本テストを追加した**

   pytestを使い、APIの起動確認、画像アップロード、レスポンス内容、不正ファイル形式のテストを追加しました。最低限の正常系と異常系を確認できるようにしています。

## このプロジェクトで学んだこと

- FastAPIを使って、画像アップロードAPIを作成する流れを学びました。
- OpenCVを使って、画像をグレースケール化・二値化する方法を学びました。
- `multipart/form-data` によるファイルアップロードの扱いを理解できました。
- 処理結果を分かりやすく返すためのJSONレスポンス設計を学びました。
- Pydantic response model を使って、API仕様を明確にする方法を学びました。
- pytestを使って、APIの基本的なテストを用意できました。
- GitHub公開を意識して、READMEを分かりやすく整理する方法を学びました。

## 現時点でできないこと

- OCRによる文字認識は未実装です。
- 画像処理のしきい値は固定値であり、画像ごとの自動調整には対応していません。
- 処理履歴のDB保存には対応していません。
- ユーザー認証やログイン機能はありません。
- クラウド環境へのデプロイは行っていません。
- アニメーションGIFの全フレーム処理には対応していません。GIFは先頭フレームのみ処理します。

## 今後の拡張案

- 一意なファイル名生成（UUIDなど）の実装
- クラウドストレージ（AWS S3等）への保存
- メタデータのDB管理への移行

## 注意事項

- このアプリはローカル実行を前提としています。
- アップロードされた画像は `output` フォルダに保存されます。
- `output` フォルダ内の処理済み画像はGit管理対象外にしています。
- GIF画像は先頭フレームのみ処理します。
- OCR機能は未実装です。

## ライセンス

このプロジェクトはポートフォリオ用途で公開しています。  
利用・改変の条件については、必要に応じて今後ライセンスを設定します。
