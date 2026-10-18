import os

from django.conf import settings


def remove_media(files: set) -> None:
    """
    Delete file from media dir
    """
    for filename in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, filename))


def remove_empty_dirs(path: str | None = None) -> bool:
    """
    Recursively delete empty directories; return True if everything was deleted.
    """

    if not path:
        path = settings.MEDIA_ROOT

    if not os.path.isdir(path):
        return False

    listdir = [os.path.join(path, filename) for filename in os.listdir(path)]

    if all(list(map(remove_empty_dirs, listdir))):
        os.rmdir(path)
        return True
    else:
        return False
