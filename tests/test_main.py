# テストで使うライブラリを読み込む

import shutil
from pathlib import Path

import cv2  # テスト用の小さな画像をメモリ上で作るために使う
import numpy as np  # 画像データを配列として用意するために使う
import pytest  # テスト用の共通準備をfixtureとして定義するために使う
from fastapi.testclient import TestClient  # FastAPIのAPIをテスト内から呼び出すために使う

import main


# APIテストで使う共通の準備を定義する

@pytest.fixture
def client(monkeypatch):  # 各テストで使うAPIクライアントを用意する
    test_output_dir = Path(__file__).parent / ".tmp_output"
    shutil.rmtree(test_output_dir, ignore_errors=True)  # 前回のテスト出力が残っていても消してから始める
    test_output_dir.mkdir()

    monkeypatch.setattr(main, "OUTPUT_DIR", test_output_dir)  # 通常のoutputフォルダではなくテスト用フォルダへ保存させる

    with TestClient(main.app) as test_client:
        yield test_client

    shutil.rmtree(test_output_dir, ignore_errors=True)  # テスト後に作成された画像を削除する


def create_test_png():  # アップロード用の小さなPNG画像をメモリ上で作る
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    image[:, :] = [255, 255, 255]
    success, encoded_image = cv2.imencode(".png", image)  # OpenCVでPNG形式のバイト列に変換する

    assert success
    return encoded_image.tobytes()


# APIの基本動作を確認する

def test_read_root_returns_health_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Image Preprocessing API is running"


def test_process_image_binary_returns_file_info(client):
    image_bytes = create_test_png()

    response = client.post(  # 生成したPNG画像をmultipart/form-dataでアップロードする
        "/process-image",
        data={"mode": "binary", "output_format": "png"},
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Image processed successfully"
    assert data["mode"] == "binary"
    assert data["output_format"] == "png"
    assert "results" in data
    assert len(data["results"]) == 1

    result = data["results"][0]  # binary指定なので保存結果は1件になる
    assert result["type"] == "binary"
    assert result["filename"]
    assert result["output_path"]
    assert result["preview_url"]
    assert result["download_url"]


def test_process_image_both_returns_two_files(client):
    image_bytes = create_test_png()

    response = client.post(  # both指定でグレースケール画像と二値化画像をまとめて作る
        "/process-image",
        data={"mode": "both", "output_format": "png"},
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["mode"] == "both"
    assert "results" in data
    assert len(data["results"]) == 2

    result_types = {result["type"] for result in data["results"]}  # 2種類の処理結果が含まれているか確認する
    assert "grayscale" in result_types
    assert "binary" in result_types

    for result in data["results"]:
        assert result["filename"]
        assert result["output_path"]
        assert result["preview_url"]
        assert result["download_url"]


def test_process_image_rejects_unsupported_file_extension(client):
    response = client.post(  # 対応していない拡張子を送って400エラーになることを確認する
        "/process-image",
        data={"mode": "binary", "output_format": "png"},
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    data = response.json()

    assert response.status_code == 400
    assert "detail" in data
