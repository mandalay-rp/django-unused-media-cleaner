import fnmatch
import os
import time

from django.conf import settings
from django.core.validators import EMPTY_VALUES

from .remove import remove_media
from .utils import get_file_fields


def get_used_media() -> set:
    """
    Get media which are still used in models
    """

    media = set()

    for field in get_file_fields():
        is_null = {
            f"{field.name}__isnull": True,
        }
        is_empty = {
            field.name: "",
        }

        storage = field.storage

        for value in (
            field.model._base_manager.values_list(field.name, flat=True)
            .exclude(**is_empty)
            .exclude(**is_null)
        ):
            if value not in EMPTY_VALUES:
                media.add(storage.path(value))

    return media


def get_all_media(
    exclude: list[str] | None = None, minimum_file_age: int | None = None
) -> set:
    """
    Get all media from MEDIA_ROOT
    """

    EXCLUDED = exclude or []

    # Паттерн со слешем на конце — исключает только каталоги
    DIR_ONLY = [p[:-1] for p in EXCLUDED if p.endswith("/")]
    # Остальные паттерны — исключают и файлы, и каталоги (как в rsync)
    BOTH = [p for p in EXCLUDED if not p.endswith("/")]

    def excluded(name, patterns):
        return any(fnmatch.fnmatchcase(name, p) for p in patterns)

    def dir_excluded(name):
        return excluded(name, DIR_ONLY) or excluded(name, BOTH)

    media = set()
    initial_time = time.time()

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        # Ключевой момент: обрезка дерева. Файлы внутри этих каталогов
        # никогда не будут перечислены.
        dirs[:] = [d for d in dirs if not dir_excluded(d)]

        for name in files:
            if excluded(name, BOTH):
                continue

            path = os.path.abspath(os.path.join(root, name))

            if minimum_file_age:
                file_age = initial_time - os.path.getmtime(path)
                if file_age < minimum_file_age:
                    continue

            media.add(path)

    return media


def get_unused_media(
    exclude: list[str] | None = None, minimum_file_age: int | None = None
) -> set:
    """
    Get media which are not used in models
    """

    if not exclude:
        exclude = []

    all_media = get_all_media(exclude, minimum_file_age)
    used_media = get_used_media()

    return all_media - used_media


def remove_unused_media() -> None:
    """
    Remove unused media
    """
    remove_media(get_unused_media())
