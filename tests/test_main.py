import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path)
    return TestClient(main.app)


def create_test_png():
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    image[:, :] = [255, 255, 255]
    success, encoded_image = cv2.imencode(".png", image)

    assert success
    return encoded_image.tobytes()


def test_read_root_returns_health_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Image Preprocessing API is running"


def test_process_image_binary_returns_file_info(client):
    image_bytes = create_test_png()

    response = client.post(
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

    result = data["results"][0]
    assert result["type"] == "binary"
    assert result["filename"]
    assert result["output_path"]
    assert result["preview_url"]
    assert result["download_url"]


def test_process_image_both_returns_two_files(client):
    image_bytes = create_test_png()

    response = client.post(
        "/process-image",
        data={"mode": "both", "output_format": "png"},
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["mode"] == "both"
    assert "results" in data
    assert len(data["results"]) == 2

    result_types = {result["type"] for result in data["results"]}
    assert "grayscale" in result_types
    assert "binary" in result_types

    for result in data["results"]:
        assert result["filename"]
        assert result["output_path"]
        assert result["preview_url"]
        assert result["download_url"]


def test_process_image_rejects_unsupported_file_extension(client):
    response = client.post(
        "/process-image",
        data={"mode": "binary", "output_format": "png"},
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    data = response.json()

    assert response.status_code == 400
    assert "detail" in data
