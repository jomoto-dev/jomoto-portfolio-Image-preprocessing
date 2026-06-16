# Image Preprocessing API

レシート画像や書類画像を、OCRなどの後続処理で扱いやすい形に変換するための画像前処理APIです。
画像をアップロードすると、グレースケール化・二値化・保存・プレビュー・ダウンロードまでをFastAPI上で実行できます。

## 作成背景


## 使用技術と選定理由

| 分類 | 技術 | 採用理由 |
|---|---|---|
| 言語 | Python | 画像処理・API開発のライブラリが豊富で、学習中のバックエンド技術と相性が良いため |
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

## デモイメージ



<table>
  <tr>
    <td><img src="<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/cb533d78-9812-417e-8d76-e91ba74fbd22" />" width="300"></td>
    <td><img src="<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/caefe977-21a3-4876-a883-8792a3d3663e" />" width="300"></td>
    <td><img src="<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/05de373f-796d-4970-bac3-09eaf35a0eb3" />" width="300"></td>
  </tr>
</table>

## セットアップ方法

```bash
git clone https://github.com//image-preprocessing-api.git（後ほど修正）
cd image-preprocessing-api

python -m venv .venv
.venv\Scripts\activate

python -m pip install -r requirements.txt
```

その後以下の方法で起動します。
```
python -m uvicorn main:app --reload
```

起動後のアクセス
<http://127.0.0.1:8000/docs>

## 使い方


## 実装した機能

- 画像アップロード
- OpenCVによるグレースケール化
- OpenCVによる二値化
- outputフォルダへの画像保存
- JSONレスポンス返却
- Pydantic response model によるレスポンス仕様の明確化
- Swagger UIでの動作確認

## 各機能の仕様紹介

・画像アップロード

- 入力対応形式: jpg / jpeg / png / gif
- 最大ファイルサイズ: 5MB
- 対応していない形式、5MBを超えるファイル、空ファイルをアップロードした場合は400エラーになります。
- GIFは先頭フレームのみ処理します。アニメーションGIFの全フレーム処理は行いません。
<img width="1485" height="668" alt="Image" src="https://github.com/user-attachments/assets/cfadb33a-f7c9-4bc4-ae6b-d797f217cee6" />

・処理モード指定

`/process-image` では、画像ファイルと一緒に `mode` を指定できます。

- `grayscale`: グレースケール化した画像を保存します。
- `binary`: グレースケール化した後、二値化した画像を保存します。
- `both`: グレースケール画像と二値化画像の両方を保存します。

`mode` を指定しない場合は、`binary` として処理されます。
Swagger UI の `/process-image` では、`mode` をプルダウンから選択して試せます。

・保存形式指定

`/process-image` では、`output_format` で保存形式を指定できます。

- `png`: png形式で保存します。
- `jpg`: jpg形式で保存します。

`output_format` を指定しない場合は、`png` として保存されます。
Swagger UI の `/process-image` では、`output_format` をプルダウンから選択して試せます。
GIFをアップロードした場合も、出力は `png` または `jpg` で保存されます。GIF形式のまま保存はしません。
<img width="1486" height="668" alt="Image" src="https://github.com/user-attachments/assets/0b92c1bf-4af7-475c-aaee-a479cbf3e087" />

・処理済み画像のダウンロード

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
<img width="1008" height="348" alt="Image" src="https://github.com/user-attachments/assets/0013fd7b-e91b-4229-9f18-9821c341a818" />

・処理済み画像のプレビュー

処理済み画像は、`GET /preview/{filename}` でブラウザ上に表示できます。

レスポンスの `results` 内にある `preview_url` を使うと、処理済み画像をそのままブラウザで確認できます。

例:

```text
GET /preview/processed_binary_xxxxx.png
```

プレビューできるのは `output` フォルダ内の png / jpg / jpeg 画像のみです。
存在しないファイル名や、`output` フォルダ外にアクセスしようとする指定は404エラーになります。
<img width="1118" height="518" alt="Image" src="https://github.com/user-attachments/assets/345e4c70-f748-42ca-ae96-dc91a40a7d77" />

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

## API仕様


## テスト実行方法

以下のコマンドでテストを実行できます。

```powershell
python -m pytest

```

## 実装時に工夫した点

## 現時点でできること

## 現時点でできないこと

## 今後の拡張案
・一意なファイル名生成（UUIDなど）の実装
・クラウドストレージ（AWS S3等）への保存
・メタデータのDB管理への移行
