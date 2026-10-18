import os
import pytest
from unused_media_cleaner.remove import remove_media, remove_empty_dirs


def test_remove_media_deletes_file(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    file = tmp_path / "to_delete.txt"
    file.write_text("content")
    remove_media({str(file)})
    assert not file.exists()


def test_remove_empty_dirs_removes_empty_tree(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    sub = tmp_path / "a" / "b"
    sub.mkdir(parents=True)
    assert remove_empty_dirs(str(tmp_path)) is True
    assert not tmp_path.exists()
