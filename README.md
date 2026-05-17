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

## フォルダ構成

```text
image-preprocessing-api/
├─ main.py
├─ requirements.txt
├─ README.md
└─ output/