# Image Preprocessing API

レシート画像や書類画像を、OCRなどの後続処理で扱いやすい形に変換するための画像前処理APIです。
画像をアップロードすると、グレースケール化・二値化・保存・プレビュー・ダウンロードまでをFastAPI上で実行できます。

## 使用技術と選定理由

| 分類 | 技術 | 採用理由 |
|---|---|---|
| 言語 | Python | 画像処理・API開発のライブラリが豊富で、学習中のバックエンド技術と相性が良いため |
| API | FastAPI | Swagger UIが自動生成され、APIの動作確認や仕様確認がしやすいため |
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
| GET | `/files` | 処理済み画像一覧をHTMLで表示する |

## セットアップ方法

### 1.リポジトリをクローン
git clone https://github.com//image-preprocessing-api.git（後ほど修正）
cd image-preprocessing-api

### 2.仮想環境の作成・有効化
python -m venv .venv
.venv\Scripts\activate

### 3.ライブラリのインストール
python -m pip install -r requirements.txt

### 4.アプリ起動
python -m uvicorn main:app --reload

## テスト実行方法

以下のコマンドでテストを実行できます。

```powershell
python -m pytest
```

## 主な機能

- 画像アップロード
- OpenCVによるグレースケール化
- OpenCVによる二値化
- outputフォルダへの画像保存
- JSONレスポンス返却
- Swagger UIでの動作確認

## アップロードできる画像

- 入力対応形式: jpg / jpeg / png / gif
- 最大ファイルサイズ: 5MB
- 対応していない形式、5MBを超えるファイル、空ファイルをアップロードした場合は400エラーになります。
- GIFは先頭フレームのみ処理します。アニメーションGIFの全フレーム処理は行いません。

## 処理モード

`/process-image` では、画像ファイルと一緒に `mode` を指定できます。

- `grayscale`: グレースケール化した画像を保存します。
- `binary`: グレースケール化した後、二値化した画像を保存します。
- `both`: グレースケール画像と二値化画像の両方を保存します。

`mode` を指定しない場合は、`binary` として処理されます。
Swagger UI の `/process-image` では、`mode` をプルダウンから選択して試せます。

## 保存形式

`/process-image` では、`output_format` で保存形式を指定できます。

- `png`: png形式で保存します。
- `jpg`: jpg形式で保存します。

`output_format` を指定しない場合は、`png` として保存されます。
Swagger UI の `/process-image` では、`output_format` をプルダウンから選択して試せます。
GIFをアップロードした場合も、出力は `png` または `jpg` で保存されます。GIF形式のまま保存はしません。

## レスポンスに含まれる情報

`/process-image` のレスポンスでは、処理結果を常に `results` 配列で返します。
`mode` が `grayscale` または `binary` の場合、`results` は1件です。
`mode` が `both` の場合、`results` は2件です。

`results` の各要素には以下の情報が含まれます。

| フィールド | 説明 |
|---|---|
| `type` | `grayscale` または `binary` |
| `filename` | 保存されたファイル名 |
| `output_path` | 保存先のパス |
| `preview_url` | ブラウザ表示用URL |
| `download_url` | ダウンロード用URL |

レスポンス例:

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

## 処理済み画像のプレビュー

処理済み画像は、`GET /preview/{filename}` でブラウザ上に表示できます。

レスポンスの `results` 内にある `preview_url` を使うと、処理済み画像をそのままブラウザで確認できます。

例:

```text
GET /preview/processed_binary_xxxxx.png
```

プレビューできるのは `output` フォルダ内の png / jpg / jpeg 画像のみです。
存在しないファイル名や、`output` フォルダ外にアクセスしようとする指定は404エラーになります。

## 処理済み画像のダウンロード

処理済み画像は、`GET /download/{filename}` でダウンロードできます。

レスポンスの `results` 内にある `filename` をそのまま `/download/{filename}` に指定して使えます。

例:

```text
GET /download/processed_binary_xxxxx.png
```

`/process-image` の `results` 内には `download_url` も含まれるため、そのURLから直接ダウンロードすることもできます。

ダウンロードできるのは `output` フォルダ内のファイルのみです。
存在しないファイル名や、`output` フォルダ外にアクセスしようとする指定は404エラーになります。

`/preview/{filename}` はブラウザで画像を表示するためのAPIです。
`/download/{filename}` は画像をファイルとしてダウンロードするためのAPIです。

## 処理済み画像の一覧ページ

`GET /files` で、`output` フォルダ内の処理済み画像をHTMLで一覧表示できます。
各ファイルのファイル名コピー、プレビュー、ダウンロードができます。
`/preview/{filename}` や `/download/{filename}` に使うファイル名を確認しやすくするための補助ページです。

## フォルダ構成

```text
image-preprocessing-api/
├─ main.py
├─ requirements.txt
├─ README.md
├─ output/
└─ tests/
   └─ test_main.py
```
