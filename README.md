# Image Preprocessing API

FastAPI と OpenCV を使った、画像前処理APIです。

レシート画像や書類画像をアップロードすると、API側で画像を受け取り、OpenCVで以下の処理を行います。

1. グレースケール化
2. 二値化
3. 処理後画像の保存
4. JSONレスポンスの返却

## 使用技術

- Python
- FastAPI
- OpenCV
- Uvicorn
- Swagger UI

## 主な機能

- 画像アップロード
- OpenCVによるグレースケール化
- OpenCVによる二値化
- outputフォルダへの画像保存
- JSONレスポンス返却
- Swagger UIでの動作確認

## アップロードできる画像

- 対応形式: jpg / jpeg / png
- 最大ファイルサイズ: 5MB
- 対応していない形式、5MBを超えるファイル、空ファイルをアップロードした場合は400エラーになります。

## 処理モード

`/process-image` では、画像ファイルと一緒に `mode` を指定できます。

- `grayscale`: グレースケール化した画像を保存します。
- `binary`: グレースケール化した後、二値化した画像を保存します。
- `both`: グレースケール画像と二値化画像の両方を保存します。

`mode` を指定しない場合は、`binary` として処理されます。
Swagger UI の `/process-image` で `mode` に `grayscale`、`binary`、`both` のいずれかを入力して試せます。
それ以外の値を入力した場合は400エラーになります。

## 保存形式

`/process-image` では、`output_format` で保存形式を指定できます。

- `png`: png形式で保存します。
- `jpg`: jpg形式で保存します。

`output_format` を指定しない場合は、`png` として保存されます。
Swagger UI の `/process-image` で `output_format` に `png` または `jpg` を入力して試せます。
それ以外の値を入力した場合は400エラーになります。

## 処理済み画像のダウンロード

処理済み画像は、`GET /download/{filename}` でダウンロードできます。

例:

```text
GET /download/processed_binary_xxxxx.png
```

`/process-image` のレスポンスには `download_url` が含まれるため、そのURLから処理済み画像を取得できます。
`mode` が `both` の場合は、`download_urls` に2つのURLが含まれます。

ダウンロードできるのは `output` フォルダ内のファイルのみです。
存在しないファイル名や、`output` フォルダ外にアクセスしようとする指定は404エラーになります。

## フォルダ構成

```text
image-preprocessing-api/
├─ main.py
├─ requirements.txt
├─ README.md
└─ output/
```
