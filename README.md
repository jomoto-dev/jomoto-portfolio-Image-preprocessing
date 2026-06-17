# Image Preprocessing API

レシート画像や書類画像を、OCRなどの後続処理で扱いやすい形に変換するための画像前処理APIです。
画像をアップロードすると、グレースケール化・二値化・保存・プレビュー・ダウンロードまでをFastAPI上で実行できま
す。

## 作成背景
pythonの実務的な使用場面のうち、画像認識機能の作成に焦点を当て、レシート画像や書類画像をOCRなどで扱う際に必要となる、グレースケール化や二値化といった基本的な前処理を行うAPIを作成しました。
ポートフォリオとして、画像処理そのものだけでなく、Web APIとして入力チェック・レスポンス設計・テストまで意識して作成しました。

## 開発方針

このアプリは、AIツールを設計相談・実装補助・エラー調査・README整理の補助として活用しながら開発しました。
ただし、生成されたコードをそのまま使うのではなく、FastAPIによる画像アップロード処理、OpenCVによるグレースケール化・二値化、レスポンス設計、テスト内容を確認し、自分で動作検証しながら実装を進めました。

DB・認証・フロントエンドはあえて追加せず、画像アップロード、画像処理、ファイル保存、レスポンス設計、テストに絞って実装しています。
機能を増やしすぎるよりも、APIとしての基本処理を理解し、面接で説明できる構成にすることを重視しました。

## デモイメージ

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/c0fc3fde-6696-440a-b6cf-35704420e953" />

<table>
  <tr>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/fe71f917-0c67-4d4a-80ff-3fd466cc12b0" />処理前</td>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/5466d266-e97b-4a56-b164-308c412507f4" />グレースケール</td>
    <td><img width="45%" alt="Image" src="https://github.com/user-attachments/assets/909b7b48-0ac2-460b-bf91-a77e6356e943" />二値</td>
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
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/cfadb33a-f7c9-4bc4-ae6b-d797f217cee6" />

### 処理モード指定

プルダウンから選択することで、`mode`による実行したい前処理の指定ができます。
- `grayscale`: グレースケール化した画像を保存します。
- `binary`: グレースケール化した後、二値化した画像を保存します。
- `both`: グレースケール画像と二値化画像の両方を保存します。

（`mode` を指定しない場合は、`binary` として処理されます。）

### 保存形式指定

プルダウンから選択することで、`output_format`による保存形式の指定ができます。

- `png`: png形式で保存します。
- `jpg`: jpg形式で保存します。

（`output_format` を指定しない場合は、`png` として保存されます  。）
（GIFをアップロードした場合も、出力は `png` または `jpg` で保存されます。）
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/0b92c1bf-4af7-475c-aaee-a479cbf3e087" />

### 処理済み画像のダウンロード

処理済み画像は、`GET /download/{filename}` でダウンロードできます。

レスポンスの `results` 内にある `filename` をそのまま `/download/{filename}` に指定して使えます。

例:

```text
GET /download/processed_binary_xxxxx.png
```

`/process-image` の `results` 内には `download_url` も含まれるため、そのURLから直接ダウンロードすることもできます。
<img width="800" alt="Image" src="https://github.com/user-attachments/assets/0013fd7b-e91b-4229-9f18-9821c341a818" />

### 処理済み画像のプレビュー

処理済み画像は、`GET /preview/{filename}` でブラウザ上に表示できます。

レスポンスの `results` 内にある `preview_url` を使うと、処理済み画像をそのままブラウザで確認できます。

例:

```text
GET /preview/processed_binary_xxxxx.png
```
<img width="1118" height="518" alt="Image" src="https://github.com/user-attachments/assets/345e4c70-f748-42ca-ae96-dc91a40a7d77" />

## API仕様

### エンドポイント一覧

| メソッド | エンドポイント | 内容 |
|---|---|---|
| GET | `/` | APIの起動確認 |
| POST | `/process-image` | 画像をアップロードして前処理を実行 |
| GET | `/preview/{filename}` | 処理済み画像をブラウザで表示 |
| GET | `/download/{filename}` | 処理済み画像をダウンロード |

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
<img width="1491" height="1055" alt="Image" src="https://github.com/user-attachments/assets/102cf2e6-502a-40d2-92a0-385d93d2e30c" />

## テスト実行方法

以下のコマンドでテストを実行できます。

```
python -m pytest
```
期待される結果:

```text
xx passed
```

## 実装時に工夫した点

- mode と output_format を選択式にし、Swagger UI上で試しやすい設計にしました。
- results 配列でレスポンス形式を統一し、処理モードに関係なく同じ構造で結果を扱えるようにしました。
- Pydantic response model を追加し、Swagger UI上でレスポンス仕様が分かりやすく表示されるようにしました。
- アップロード可能な拡張子とファイルサイズを制限し、不正な入力に対して400エラーを返すようにしました。
- output フォルダ外のファイルにアクセスされないよう、保存済み画像の取得時に安全なパスチェックを行っています。
- pytestを使い、起動確認・画像アップロード・レスポンス内容・不正ファイル形式の基本テストを追加しました。

## このプロジェクトで学んだこと

- FastAPIで画像アップロードAPIを作成する方法
- OpenCVで画像をグレースケール化・二値化する方法
- multipart/form-data によるファイルアップロードの扱い
- JSONレスポンスの設計
- Pydantic response model によるAPI仕様の明確化
- pytestによるAPIテストの基本
- GitHub公開を意識したREADMEの整理

## 現時点でできること

- jpg / jpeg / png / gif 画像をアップロードできます。
- アップロード画像をグレースケール化できます。
- アップロード画像を二値化できます。
- グレースケール画像と二値化画像の両方を保存できます。
- 保存形式を png / jpg から選択できます。
- 処理済み画像をブラウザでプレビューできます。
- 処理済み画像をダウンロードできます。
- Swagger UIからAPIを操作できます。
- pytestで基本的なAPIテストを実行できます。

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
