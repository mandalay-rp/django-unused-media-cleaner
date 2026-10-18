import os

import pytest

from unused_media_cleaner.cleanup import (
    get_all_media,
    get_unused_media,
    get_used_media,
)


@pytest.mark.django_db
def test_get_used_media_empty_when_no_models():
    assert get_used_media() == set()


@pytest.mark.django_db
def test_get_used_media_returns_file_paths(db_media):
    used = get_used_media()
    assert len(used) == 1
    assert os.path.exists(next(iter(used)))


def test_get_all_media_finds_files(media_root):
    path = os.path.join(media_root, "a.txt")
    with open(path, "w") as f:
        f.write("x")
    assert path in get_all_media()


def test_get_all_media_excludes_patterns(media_root):
    path = os.path.join(media_root, "a.txt")
    with open(path, "w") as f:
        f.write("x")
    assert path not in get_all_media(exclude=["*.txt"])


@pytest.mark.django_db
def test_get_unused_media_returns_orphan_files(media_file):
    assert media_file in get_unused_media()


@pytest.mark.django_db
def test_get_unused_media_excludes_used_files(db_media, media_root):
    unused = get_unused_media()
    assert len(unused) == 0, unused
