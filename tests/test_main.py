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
    assert data["filename"]
    assert data["output_path"]
    assert data["preview_url"]
    assert data["download_url"]


def test_process_image_both_returns_two_files(client):
    image_bytes = create_test_png()

    response = client.post(
        "/process-image",
        data={"mode": "both", "output_format": "png"},
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data["filenames"]) == 2
    assert len(data["output_paths"]) == 2
    assert len(data["preview_urls"]) == 2
    assert len(data["download_urls"]) == 2


def test_process_image_rejects_unsupported_file_extension(client):
    response = client.post(
        "/process-image",
        data={"mode": "binary", "output_format": "png"},
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    data = response.json()

    assert response.status_code == 400
    assert "detail" in data
