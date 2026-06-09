from enum import Enum
from html import escape
from io import BytesIO
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse


app = FastAPI(
    title="Image Preprocessing API",
    description="Uploaded images are converted to grayscale and thresholded using OpenCV.",
    version="1.0.0",
)

# 処理後の画像を保存するフォルダ
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# アップロードを許可する拡張子と最大ファイルサイズです
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024
PREVIEW_EXTENSIONS = {".png", ".jpg", ".jpeg"}


class ProcessingMode(str, Enum):
    grayscale = "grayscale"
    binary = "binary"
    both = "both"


class OutputFormat(str, Enum):
    png = "png"
    jpg = "jpg"


def get_safe_output_path(filename: str):
    """
    outputフォルダ内の安全なファイルパスだけを返します。
    """

    safe_filename = Path(filename).name
    if not safe_filename:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    output_dir = OUTPUT_DIR.resolve()
    requested_path = (output_dir / safe_filename).resolve()

    try:
        requested_path.relative_to(output_dir)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    if not requested_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return requested_path


def load_image_from_upload(image_bytes: bytes, extension: str):
    """
    アップロードされた画像をOpenCVで扱えるBGR形式に変換します。
    GIFの場合は先頭フレームだけを読み込みます。
    """

    if extension == ".gif":
        try:
            from PIL import Image, UnidentifiedImageError

            with Image.open(BytesIO(image_bytes)) as gif_image:
                gif_image.seek(0)
                rgb_image = gif_image.convert("RGB")
                rgb_array = np.array(rgb_image)
                image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        except ImportError:
            raise HTTPException(
                status_code=500,
                detail="Pillow is required to read GIF images.",
            )
        except (UnidentifiedImageError, OSError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Could not read the uploaded GIF image.",
            )

        return image, ["loaded_first_gif_frame"]

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded image.",
        )

    return image, []


def get_processed_image_filenames():
    """
    outputフォルダ内の処理済み画像ファイル名だけを返します。
    """

    filenames = []
    output_dir = OUTPUT_DIR.resolve()

    for path in output_dir.iterdir():
        if not path.is_file() or path.suffix.lower() not in PREVIEW_EXTENSIONS:
            continue

        try:
            get_safe_output_path(path.name)
        except HTTPException:
            continue

        filenames.append(path.name)

    return sorted(filenames)


@app.get("/")
def read_root():
    """
    動作確認用の簡単なエンドポイントです。
    ブラウザで http://127.0.0.1:8000/ にアクセスすると確認できます。
    """
    return {"message": "Image Preprocessing API is running"}


@app.get("/files", response_class=HTMLResponse)
def list_processed_files():
    """
    outputフォルダ内の処理済み画像を一覧表示するページです。
    """

    filenames = get_processed_image_filenames()

    if filenames:
        file_items = []
        for filename in filenames:
            escaped_filename = escape(filename, quote=True)
            encoded_filename = quote(filename)
            file_items.append(
                f"""
                <li class="file-item">
                    <span class="filename">{escaped_filename}</span>
                    <button type="button" data-filename="{escaped_filename}">Copy filename</button>
                    <a href="/preview/{encoded_filename}" target="_blank">Preview</a>
                    <a href="/download/{encoded_filename}">Download</a>
                </li>
                """
            )

        files_html = f"<ul>{''.join(file_items)}</ul>"
    else:
        files_html = "<p>処理済みファイルはまだありません。</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>Processed Files</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 32px;
                color: #222;
            }}
            h1 {{
                font-size: 24px;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            .file-item {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 10px 0;
                border-bottom: 1px solid #ddd;
            }}
            .filename {{
                min-width: 320px;
                font-family: Consolas, monospace;
            }}
            button, a {{
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <h1>Processed Files</h1>
        {files_html}
        <script>
            document.querySelectorAll("button[data-filename]").forEach((button) => {{
                button.addEventListener("click", async () => {{
                    await navigator.clipboard.writeText(button.dataset.filename);
                    button.textContent = "Copied";
                    setTimeout(() => {{
                        button.textContent = "Copy filename";
                    }}, 1200);
                }});
            }});
        </script>
    </body>
    </html>
    """


@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    mode: ProcessingMode = Form(ProcessingMode.binary),
    output_format: OutputFormat = Form(OutputFormat.png),
):
    """
    画像をアップロードして、OpenCVで前処理するAPIです。

    処理の流れ:
    1. 画像ファイルを受け取る
    2. modeとoutput_formatを確認する
    3. OpenCVで読み込む
    4. modeに合わせてグレースケール化や二値化をする
    5. outputフォルダに保存する
    6. JSONで結果を返す
    """

    mode_value = mode.value
    output_format_value = output_format.value

    file_extension = Path(file.filename or "").suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only jpg, jpeg, png, and gif image files can be uploaded.",
        )

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
            detail="The uploaded file is empty. Please choose an image file that has data.",
        )

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is too large. Please upload an image that is 5MB or smaller.",
        )

    # バイト列をOpenCVで扱える形式に変換します
    image, image_load_steps = load_image_from_upload(image_bytes, file_extension)

    # グレースケール化: カラー画像を白黒の濃淡画像に変換します
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    filenames = []
    output_paths = []
    download_urls = []
    preview_urls = []

    if mode_value in {"grayscale", "both"}:
        # uuid4を使うことで、同じ名前の画像が上書きされにくくなります
        grayscale_filename = f"processed_grayscale_{uuid4().hex}.{output_format_value}"
        grayscale_path = OUTPUT_DIR / grayscale_filename
        saved = cv2.imwrite(str(grayscale_path), gray_image)

        if not saved:
            raise HTTPException(
                status_code=500,
                detail="Failed to save processed image.",
            )

        filenames.append(grayscale_filename)
        output_paths.append(str(grayscale_path).replace("\\", "/"))
        download_urls.append(f"/download/{grayscale_filename}")
        preview_urls.append(f"/preview/{grayscale_filename}")

    if mode_value in {"binary", "both"}:
        # 二値化: 画像を白と黒の2色に分けます
        # しきい値127より大きい部分を255、そうでない部分を0にします
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        binary_filename = f"processed_binary_{uuid4().hex}.{output_format_value}"
        binary_path = OUTPUT_DIR / binary_filename
        saved = cv2.imwrite(str(binary_path), binary_image)

        if not saved:
            raise HTTPException(
                status_code=500,
                detail="Failed to save processed image.",
            )

        filenames.append(binary_filename)
        output_paths.append(str(binary_path).replace("\\", "/"))
        download_urls.append(f"/download/{binary_filename}")
        preview_urls.append(f"/preview/{binary_filename}")

    steps = [
        "uploaded",
        *image_load_steps,
        "converted_to_grayscale",
    ]

    if mode_value in {"binary", "both"}:
        steps.append("applied_threshold")

    steps.append("saved_output_image")

    # JSONで処理結果を返します
    response = {
        "message": "Image processed successfully",
        "mode": mode_value,
        "output_format": output_format_value,
        "steps": steps,
    }

    if mode_value == "both":
        response["filenames"] = filenames
        response["output_paths"] = output_paths
        response["download_urls"] = download_urls
        response["preview_urls"] = preview_urls
    else:
        response["filename"] = filenames[0]
        response["output_path"] = output_paths[0]
        response["download_url"] = download_urls[0]
        response["preview_url"] = preview_urls[0]

    return response


@app.get("/download/{filename}")
def download_image(filename: str):
    """
    outputフォルダに保存された処理済み画像をダウンロードするAPIです。
    """

    requested_path = get_safe_output_path(filename)
    return FileResponse(path=requested_path, filename=requested_path.name)


@app.get("/preview/{filename}")
def preview_image(filename: str):
    """
    outputフォルダに保存された処理済み画像をブラウザで表示するAPIです。
    """

    requested_path = get_safe_output_path(filename)

    if requested_path.suffix.lower() not in PREVIEW_EXTENSIONS:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return FileResponse(path=requested_path)
