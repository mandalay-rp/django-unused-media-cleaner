import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.testapp.models import MediaModel


@pytest.fixture
def media_root(settings, tmp_path):
    """Изолированный MEDIA_ROOT на каждый тест. Только str — так безопаснее."""
    root = str(tmp_path / "media")
    os.makedirs(root, exist_ok=True)
    settings.MEDIA_ROOT = root
    return root


@pytest.fixture
def media_file(media_root):
    """Реальный файл в MEDIA_ROOT, не связанный ни с одной моделью."""
    path = os.path.join(media_root, "test.txt")
    with open(path, "w") as f:
        f.write("test content")
    return path


@pytest.fixture
def db_media(db, media_root):
    """Модель с файлом — файл считается используемым."""
    upload = SimpleUploadedFile("test.txt", b"test content")
    obj = MediaModel.objects.create(file=upload)
    return obj
