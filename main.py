from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile


app = FastAPI(
    title="Image Preprocessing API",
    description="Uploaded images are converted to grayscale and thresholded using OpenCV.",
    version="1.0.0",
)

# 処理後の画像を保存するフォルダ
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
def read_root():
    """
    動作確認用の簡単なエンドポイントです。
    ブラウザで http://127.0.0.1:8000/ にアクセスすると確認できます。
    """
    return {"message": "Image Preprocessing API is running"}


@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """
    画像をアップロードして、OpenCVで前処理するAPIです。

    処理の流れ:
    1. 画像ファイルを受け取る
    2. OpenCVで読み込む
    3. グレースケール化する
    4. 二値化する
    5. outputフォルダに保存する
    6. JSONで結果を返す
    """

    # 画像ファイルかどうかを簡単にチェックします
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    # アップロードされた画像ファイルをバイト列として読み込みます
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # バイト列をOpenCVで扱える形式に変換します
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # OpenCVで画像として読み込めなかった場合
    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded image.",
        )

    # グレースケール化: カラー画像を白黒の濃淡画像に変換します
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二値化: 画像を白と黒の2色に分けます
    # しきい値127より大きい部分を255、そうでない部分を0にします
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # 保存ファイル名を作ります
    # uuid4を使うことで、同じ名前の画像が上書きされにくくなります
    output_filename = f"processed_{uuid4().hex}.png"
    output_path = OUTPUT_DIR / output_filename

    # 処理後の画像をoutputフォルダに保存します
    saved = cv2.imwrite(str(output_path), binary_image)

    if not saved:
        raise HTTPException(
            status_code=500,
            detail="Failed to save processed image.",
        )

    # JSONで処理結果を返します
    return {
        "message": "Image processed successfully",
        "steps": [
            "uploaded",
            "converted_to_grayscale",
            "applied_threshold",
            "saved_output_image",
        ],
        "output_path": str(output_path).replace("\\", "/"),
    }